"""
O grande final: o dossiê da Operação Vitrine Fantasma, gerado inteiro por código.

Carta 42 (rank A) — Jutsu do Revisor (o dossiê)

O que você aprende (juntando os 21 dias):
  • RDAP + WHOIS (Dia 15): idade do domínio na 1ª vítima;
  • dump .sql no sqlite3 (Dia 8): quanto cada conta laranja recebeu;
  • CSV + padronização de cidades (Dias 7, 13, 16): onde estão as vítimas;
  • regex + dígito verificador (Dias 2, 11): os CNPJs citados pelo vendedor;
  • Wayback + datas (Dia 19): a linha do tempo e a Black Friday;
  • hashes SHA-256 (Dia 14) e relatório HTML (Dias 17 e 18): tudo auditável;
  • e autoverificações (Dia 21): o dossiê confere os próprios números antes de ser gravado.

100% offline e só com a biblioteca padrão.

Como rodar (dentro da pasta dia-21-ferramentas-de-codigo):
    python br/03_dossie_final.py
    (abra saidas/dossie.html no navegador; para PDF, Ctrl+P → Salvar como PDF)
"""

import calendar
import csv
import difflib
import hashlib
import html
import json
import re
import sqlite3
import unicodedata
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
ANALISTA = "Analista NFA"  #@param {type:"string"}
DESTINATARIA = "Delegada Rita Assunção"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"

try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))

e = html.escape
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]
CIDADES_OFICIAIS = ["Belo Horizonte", "Betim", "Contagem", "Divinópolis", "Governador Valadares",
                    "Ipatinga", "Juiz de Fora", "Poços de Caldas", "Sete Lagoas", "Uberaba", "Uberlândia"]


# ── Ferramentas dos dias anteriores, em forma de função ───────────────────
def reais(v):                                                   # Dia 17
    return "R$ " + f"{v:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")


def br(d):                                                      # Dia 19
    return f"{d:%d/%m/%Y}"


def chave(t):                                                   # Dia 16
    s = "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))
    return " ".join(s.casefold().split())


OFICIAIS = {chave(c): c for c in CIDADES_OFICIAIS}


def padronizar(cidade):                                         # Dia 7
    k = chave(cidade)
    if k in OFICIAIS:
        return OFICIAIS[k]
    p = difflib.get_close_matches(k, OFICIAIS, n=1, cutoff=0.8)
    return OFICIAIS[p[0]] if p else cidade


def cnpj_valido(cnpj):                                          # Dia 2
    """Aceita o formato numérico e o alfanumérico (valor = ord(c) - 48)."""
    c = re.sub(r"[^0-9A-Z]", "", cnpj.upper())
    if len(c) != 14 or not c[12:].isdigit() or len(set(c)) == 1:
        return False
    valores = [ord(x) - 48 for x in c]
    for n, pesos in ((12, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]), (13, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])):
        resto = sum(v * p for v, p in zip(valores, pesos)) % 11
        if (0 if resto < 2 else 11 - resto) != valores[n]:
            return False
    return True


def sha256(caminho):                                            # Dia 14
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def black_friday(ano):                                          # Dia 19
    quintas = [s[calendar.THURSDAY] for s in calendar.monthcalendar(ano, 11) if s[calendar.THURSDAY]]
    return date(ano, 11, quintas[3]) + timedelta(days=1)


# ── 1. Domínio (RDAP × WHOIS) ─────────────────────────────────────────────
ficha = json.loads((PASTA_CASO / "ficha_do_caso.json").read_text(encoding="utf-8"))
rdap = json.loads((PASTA_CASO / "rdap_megaoferta.json").read_text(encoding="utf-8"))
eventos_rdap = {ev["eventAction"]: ev["eventDate"] for ev in rdap["events"]}
criado = datetime.fromisoformat(eventos_rdap["registration"].replace("Z", "+00:00")).date()
titular_rdap = next(c[3] for ent in rdap["entities"] for c in ent["vcardArray"][1] if c[0] == "fn")
whois = (PASTA_CASO / "whois_megaoferta.txt").read_text(encoding="utf-8")
criado_whois = datetime.strptime(re.search(r"^created:\s+(\d{8})", whois, re.M).group(1), "%Y%m%d").date()
nameservers = [ns["ldhName"] for ns in rdap.get("nameservers", [])]

# ── 2. Denúncias ──────────────────────────────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as f:
    denuncias = list(csv.DictReader(f, delimiter=";"))
total_denuncias = sum(Decimal(d["valor"]) for d in denuncias)
datas = sorted(date.fromisoformat(d["data"]) for d in denuncias)
cidades = Counter(padronizar(d["cidade"]) for d in denuncias)

# ── 3. Dump do painel (sqlite3 em memória) ────────────────────────────────
banco = sqlite3.connect(":memory:")
banco.executescript((PASTA_CASO / "painel_dump.sql").read_text(encoding="utf-8"))
laranjas = banco.execute("""
    SELECT c.titular, c.banco, c.chave_pix, COUNT(p.id), ROUND(SUM(p.valor), 2)
    FROM pedidos p JOIN contas_recebimento c ON c.id = p.conta_id
    GROUP BY c.id ORDER BY SUM(p.valor) DESC
""").fetchall()
total_dump = Decimal(str(banco.execute("SELECT ROUND(SUM(valor), 2) FROM pedidos").fetchone()[0]))
banco.close()

# ── 4. Conversa: CNPJs citados pelo vendedor ──────────────────────────────
conversa = (PASTA_CASO / "conversa_whatsapp.txt").read_text(encoding="utf-8")
cnpjs = sorted(set(re.findall(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b", conversa)))

# ── 5. Wayback + linha do tempo ───────────────────────────────────────────
cab, *linhas_cdx = json.loads((PASTA_CASO / "wayback_cdx_megaoferta.json").read_text(encoding="utf-8"))
capturas = [dict(zip(cab, l)) for l in linhas_cdx]
bf = black_friday(2025)
perto_bf = sum(1 for d in datas if abs((d - bf).days) <= 3)

linha_do_tempo = [(criado, "Domínio registrado (RDAP e WHOIS concordam)" if criado == criado_whois
                   else "Domínio registrado (RDAP e WHOIS DISCORDAM)")]
linha_do_tempo += [(datas[0], "Primeira denúncia"), (bf, "Black Friday 2025"), (datas[-1], "Última denúncia")]
for c in capturas:
    dia = datetime.strptime(c["timestamp"], "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc).astimezone(FUSO).date()
    linha_do_tempo.append((dia, f"Captura Wayback: HTTP {c['statuscode']}, {c['length']} bytes"))
linha_do_tempo.sort()

# ── 6. Evidências com hash ────────────────────────────────────────────────
evidencias = [(p.relative_to(PASTA_CASO).as_posix(), p.stat().st_size, sha256(p))
              for p in sorted(PASTA_CASO.rglob("*")) if p.is_file()]

# ── 7. Autoverificação: o dossiê confere a si mesmo ───────────────────────
# Se alguma fonte for alterada e os números deixarem de bater, o dossiê NÃO é gerado.
checagens = [
    ("Total de denúncias bate com a ficha do caso", len(denuncias) == ficha["total_denuncias"]),
    ("Soma das denúncias = soma dos pedidos no dump", total_denuncias == total_dump),
    ("RDAP e WHOIS concordam na data de criação", criado == criado_whois),
    ("CNPJ do rodapé é inválido (DV não fecha)", not cnpj_valido(ficha["cnpj_rodape"])),
    ("As 3 chaves do dump são as 3 chaves da ficha", {l[2] for l in laranjas} == set(ficha["chaves_pix"])),
    ("Todas as cidades foram padronizadas", all(c in CIDADES_OFICIAIS for c in cidades)),
]
print("🔎 Autoverificação do dossiê:")
for descricao, ok in checagens:
    print(f"   {'✅' if ok else '❌'} {descricao}")
if not all(ok for _, ok in checagens):
    raise SystemExit("❌ Os números não fecham. Corrija antes de entregar o dossiê.")

# ── 8. Escrever o HTML ────────────────────────────────────────────────────
agora = datetime.now(FUSO)
maior_cidade = max(cidades.values())


def tabela(cabecalho, linhas):
    th = "".join(f"<th>{e(c)}</th>" for c in cabecalho)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in linha) + "</tr>" for linha in linhas)
    return f"<table><tr>{th}</tr>{trs}</table>"


secao_laranjas = tabela(["Titular", "Instituição", "Chave PIX", "Pedidos", "Valor"],
                        [(e(t), e(b), f"<code>{e(c)}</code>", n, f"<span class='num'>{reais(Decimal(str(v)))}</span>")
                         for t, b, c, n, v in laranjas])
secao_cidades = "".join(
    f"<div class='barra'><span>{e(c)}</span><i style='width:{q / maior_cidade * 100:.0f}%'></i><b>{q}</b></div>"
    for c, q in cidades.most_common())
secao_cnpjs = tabela(["CNPJ citado na conversa", "Dígito verificador"],
                     [(f"<code>{e(c)}</code>", "✅ válido" if cnpj_valido(c) else "❌ inválido") for c in cnpjs])
secao_tempo = tabela(["Data", "D+", "Evento"], [(br(d), (d - criado).days, e(t)) for d, t in linha_do_tempo])
secao_hash = tabela(["Arquivo", "Bytes", "SHA-256"],
                    [(e(n), f"<span class='num'>{t}</span>", f"<code>{h}</code>") for n, t, h in evidencias])
secao_checagens = "".join(f"<li>{'✅' if ok else '❌'} {e(d)}</li>" for d, ok in checagens)

pagina = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dossiê — Operação Vitrine Fantasma</title>
<style>
 :root {{ --azul: #1f5fa8; --texto: #1d2433; --cinza: #5b6475; --linha: #d5dbe5; }}
 body {{ font-family: system-ui, sans-serif; color: var(--texto); max-width: 980px; margin: 2rem auto; padding: 0 1rem; line-height: 1.45; }}
 header {{ border-bottom: 4px solid var(--azul); margin-bottom: 1.5rem; }}
 h1 {{ margin: .2rem 0; }} h2 {{ color: var(--azul); margin-top: 2rem; }}
 .meta {{ color: var(--cinza); font-size: .9rem; }}
 .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: .8rem; }}
 .card {{ background: #eef3fa; border-radius: 8px; padding: .7rem 1rem; }}
 .card b {{ display: block; font-size: 1.5rem; color: var(--azul); }}
 table {{ border-collapse: collapse; width: 100%; font-size: .88rem; margin: .5rem 0; }}
 th, td {{ border-bottom: 1px solid var(--linha); padding: .35rem .5rem; text-align: left; vertical-align: top; }}
 th {{ background: var(--azul); color: #fff; }} .num {{ white-space: nowrap; }}
 code {{ font-size: .78rem; word-break: break-all; }}
 .barra {{ display: grid; grid-template-columns: 170px 1fr 30px; align-items: center; gap: .5rem; margin: .2rem 0; }}
 .barra i {{ display: block; height: 16px; background: var(--azul); border-radius: 3px; }}
 .aviso {{ border-left: 4px solid #b3261e; background: #fbeeee; padding: .6rem 1rem; }}
 footer {{ margin-top: 2.5rem; color: var(--cinza); font-size: .8rem; border-top: 1px solid var(--linha); padding-top: .8rem; }}
 @media print {{ th {{ background: #ddd; color: #000; }} .barra i {{ background: #555; }} h2 {{ break-after: avoid; }} }}
</style></head>
<body>
<header>
 <div class="meta">NÚCLEO DE FONTES ABERTAS · uso restrito · dados fictícios de estudo</div>
 <h1>Dossiê — Operação Vitrine Fantasma</h1>
 <div class="meta">Para: {e(DESTINATARIA)} · Responsável: {e(ANALISTA)} ·
 Gerado em {agora.day} de {MESES[agora.month - 1]} de {agora.year}, {agora:%H:%M} (Brasília, UTC{agora:%z})</div>
</header>

<h2>1. Resumo executivo</h2>
<div class="cards">
 <div class="card"><b>{len(denuncias)}</b>vítimas em {len(cidades)} cidades de MG</div>
 <div class="card"><b>{reais(total_denuncias)}</b>prejuízo declarado</div>
 <div class="card"><b>{(datas[0] - criado).days} dias</b>de vida do domínio na 1ª vítima</div>
 <div class="card"><b>{len(laranjas)}</b>contas de recebimento</div>
 <div class="card"><b>{perto_bf / len(datas):.0%}</b>das denúncias em ±3 dias da Black Friday</div>
</div>
<p>A loja <code>{e(ficha['dominio'])}</code> foi registrada em {br(criado)} em nome de
<b>{e(titular_rdap)}</b>, anunciou eletrônicos muito abaixo do preço com pagamento exclusivo por PIX,
recebeu {len(denuncias)} pagamentos entre {br(datas[0])} e {br(datas[-1])}, passou a exibir uma página
mínima em 01/12/2025 e saiu do ar (HTTP 404) em 05/12/2025.</p>

<h2>2. Domínio</h2>
<ul>
 <li>Criação: RDAP {br(criado)} · WHOIS {br(criado_whois)} ({'as fontes concordam' if criado == criado_whois else 'DIVERGÊNCIA'})</li>
 <li>Titular declarado no registro: {e(titular_rdap)}</li>
 <li>Servidores DNS: {e(', '.join(nameservers))}</li>
 <li>CNPJ do rodapé {e(ficha['cnpj_rodape'])}: {'válido' if cnpj_valido(ficha['cnpj_rodape']) else '<b>dígito verificador inválido</b>'}</li>
</ul>

<h2>3. Para onde foi o dinheiro (dump do painel)</h2>
{secao_laranjas}
<p class="meta">Total no dump: {reais(total_dump)}, idêntico ao total declarado pelas vítimas.</p>
<p class="aviso">Hipótese a verificar: o titular "M. R. Brandão Comércio ME" tem o mesmo sobrenome que o
titular do domínio. Sobrenome igual <b>não</b> comprova vínculo.</p>

<h2>4. CNPJs citados pelo vendedor</h2>
{secao_cnpjs}

<h2>5. Onde estão as vítimas</h2>
{secao_cidades}

<h2>6. Linha do tempo</h2>
{secao_tempo}

<h2>7. Integridade das evidências</h2>
<p>SHA-256 de cada arquivo usado neste dossiê. Qualquer pessoa pode recalcular e confirmar que nada mudou.</p>
{secao_hash}

<h2>8. Autoverificação</h2>
<ul>{secao_checagens}</ul>

<h2>9. Limitações e próximos passos</h2>
<ul>
 <li>Os dados de registro do domínio e o nome dos titulares das contas são <b>declarados</b>: podem ser falsos ou de laranjas.</li>
 <li>As capturas da Wayback não cobrem todos os dias; há lacunas de até 30 dias sem prova direta do conteúdo do site.</li>
 <li>Sugere-se ofício às três instituições de pagamento e ao registrador do domínio.</li>
</ul>

<footer>Gerado por <code>br/03_dossie_final.py</code> (só biblioteca padrão do Python) a partir de
<code>caso/dados/</code>. Rodar de novo com os mesmos arquivos produz os mesmos números.</footer>
</body></html>
"""

SAIDAS.mkdir(exist_ok=True)
destino = SAIDAS / "dossie.html"
destino.write_text(pagina, encoding="utf-8")
hash_dossie = hashlib.sha256(pagina.encode("utf-8")).hexdigest()

print(f"\n📁 {destino.relative_to(PASTA_DIA)} gravado ({len(pagina):,} caracteres)".replace(",", "."))
print(f"🔏 SHA-256 do dossiê: {hash_dossie}")
print(f"   {len(denuncias)} vítimas · {reais(total_denuncias)} · {len(laranjas)} contas · domínio com "
      f"{(datas[0] - criado).days} dias na 1ª vítima")
print("📨 Pronto para entregar. Abra no navegador; para PDF, Ctrl+P → Salvar como PDF.")

if "__file__" not in globals():
    try:
        from IPython.display import HTML, display
        display(HTML(pagina))
    except ImportError:
        pass
