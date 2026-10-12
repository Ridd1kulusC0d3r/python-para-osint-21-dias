"""
Relatório em HTML com tabela, totais, hashes SHA-256 e carimbo de tempo.

Carta 38 (rank A) — Jutsu do Relatório Automático (parte 2)

O que você aprende:
  • a montar uma página HTML só com strings (sem instalar nada);
  • a escapar o texto com html.escape (um nome com "<" não pode quebrar a página);
  • a incluir o SHA-256 de cada evidência no próprio relatório (cadeia de custódia, Dia 14);
  • a gerar PDF sem biblioteca: abrir no navegador e "Imprimir → Salvar como PDF".

Como rodar (dentro da pasta dia-17-documentos):
    python br/02_relatorio_html.py
    (depois abra saidas/relatorio_preliminar.html no navegador)
"""

import csv
import hashlib
import html                          # html.escape: transforma < > & " em texto seguro
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
TITULO = "Operação Vitrine Fantasma — relatório preliminar"  #@param {type:"string"}
ANALISTA = "Analista NFA"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"

try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:                    # Windows sem tzdata
    FUSO = timezone(timedelta(hours=-3))


def reais(valor):
    return "R$ " + f"{valor:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")


def sha256(caminho):
    """Hash SHA-256 lendo em blocos de 64 KB (funciona até com arquivos enormes)."""
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


e = html.escape   # apelido curto: vamos usar muito

# ── 1. Dados ──────────────────────────────────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    denuncias = sorted(csv.DictReader(arquivo, delimiter=";"), key=lambda d: d["data"])
total = sum(Decimal(d["valor"]) for d in denuncias)

evidencias = sorted(p for p in PASTA_CASO.rglob("*") if p.is_file())

# ── 2. Linhas da tabela de denúncias ──────────────────────────────────────
linhas_denuncias = []
for d in denuncias:
    dia, mes, ano = d["data"][8:10], d["data"][5:7], d["data"][:4]
    linhas_denuncias.append(
        "<tr>"
        f"<td>{e(d['id'])}</td><td>{dia}/{mes}/{ano}</td>"
        f"<td>{e(d['cidade'])}</td><td>{e(d['produto'])}</td>"
        f"<td class='num'>{reais(Decimal(d['valor']))}</td>"
        f"<td><code>{e(d['chave_pix_destino'][:8])}…</code></td>"
        "</tr>"
    )
    # Repare: o NOME e o CPF das vítimas ficam FORA do relatório. Minimização (LGPD):
    # quem lê o relatório preliminar não precisa deles para entender o golpe.

linhas_hash = [
    f"<tr><td>{e(p.relative_to(PASTA_CASO).as_posix())}</td>"
    f"<td class='num'>{p.stat().st_size:,}".replace(",", ".") + " B</td>"
    f"<td><code>{sha256(p)}</code></td></tr>"
    for p in evidencias
]

agora = datetime.now(FUSO)

# ── 3. A página ───────────────────────────────────────────────────────────
# Chaves {{ }} duplas: dentro de uma f-string, "{{" vira "{" literal (necessário no CSS).
pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{e(TITULO)}</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; color: #1d2433; }}
  h1 {{ border-bottom: 3px solid #1f5fa8; padding-bottom: .4rem; }}
  .cards {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
  .card {{ flex: 1; min-width: 180px; background: #eef3fa; border-radius: 8px; padding: .8rem 1rem; }}
  .card b {{ display: block; font-size: 1.6rem; color: #1f5fa8; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: .9rem; }}
  th, td {{ border-bottom: 1px solid #d5dbe5; padding: .35rem .5rem; text-align: left; }}
  th {{ background: #1f5fa8; color: white; }}
  .num {{ text-align: right; white-space: nowrap; }}
  code {{ font-size: .8rem; word-break: break-all; }}
  footer {{ margin-top: 2rem; font-size: .8rem; color: #5b6475; }}
  @media print {{ th {{ color: black; background: #ddd; }} .card {{ border: 1px solid #999; }} }}
</style>
</head>
<body>
<h1>{e(TITULO)}</h1>
<p>Gerado em <b>{agora:%d/%m/%Y %H:%M:%S}</b> (horário de Brasília, UTC{agora:%z}) · Responsável: {e(ANALISTA)}</p>

<div class="cards">
  <div class="card"><b>{len(denuncias)}</b>denúncias</div>
  <div class="card"><b>{reais(total)}</b>prejuízo declarado</div>
  <div class="card"><b>{len({d['chave_pix_destino'] for d in denuncias})}</b>chaves PIX de destino</div>
  <div class="card"><b>{len(evidencias)}</b>arquivos de evidência</div>
</div>

<h2>Denúncias (ordem cronológica)</h2>
<table>
<tr><th>ID</th><th>Data</th><th>Cidade (como digitada)</th><th>Produto</th><th>Valor</th><th>Chave PIX</th></tr>
{chr(10).join(linhas_denuncias)}
</table>

<h2>Integridade das evidências (SHA-256)</h2>
<p>Qualquer pessoa pode recalcular estes hashes e confirmar que os arquivos não mudaram desde a geração deste relatório.</p>
<table>
<tr><th>Arquivo</th><th>Tamanho</th><th>SHA-256</th></tr>
{chr(10).join(linhas_hash)}
</table>

<footer>Relatório gerado por <code>br/02_relatorio_html.py</code> · Dados fictícios de estudo · Para PDF: Ctrl+P → Salvar como PDF.</footer>
</body>
</html>
"""

SAIDAS.mkdir(exist_ok=True)
destino = SAIDAS / "relatorio_preliminar.html"
destino.write_text(pagina, encoding="utf-8")
print(f"🧾 {len(denuncias)} denúncias · {reais(total)} · {len(evidencias)} evidências com hash")
print(f"💾 {destino.relative_to(PASTA_DIA)} gravado ({len(pagina):,} caracteres).".replace(",", "."))
print("🖨️ Abra no navegador e use Imprimir → Salvar como PDF.")

# No Colab/Jupyter (onde não existe __file__), mostra a página logo abaixo da célula.
if "__file__" not in globals():
    try:
        from IPython.display import HTML, display
        display(HTML(pagina))
    except ImportError:
        pass
