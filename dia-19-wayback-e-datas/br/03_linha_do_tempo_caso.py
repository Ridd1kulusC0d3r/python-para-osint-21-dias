"""
Caso Vitrine Fantasma: a linha do tempo do golpe e o efeito Black Friday.

Carta 40 (rank A) — Jutsu da Linha do Tempo (aplicação no caso)

O que você aprende:
  • a juntar eventos de fontes diferentes (RDAP, Wayback, denúncias) numa única linha do tempo;
  • a ler o "length" das capturas: página que encolhe de repente = "em manutenção";
  • a calcular a Black Friday com o módulo calendar (o dia seguinte à 4ª quinta-feira de novembro);
  • a medir a concentração de denúncias perto dela.

100% offline: usa os dados fictícios de caso/dados/.

Como rodar (dentro da pasta dia-19-wayback-e-datas):
    python br/03_linha_do_tempo_caso.py
"""

import calendar
import csv
import json
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
JANELA_DIAS = 3  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"

try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))

DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]


def black_friday(ano):
    """Black Friday = a sexta-feira logo depois da 4ª quinta-feira de novembro (o Thanksgiving dos EUA).

    calendar.monthcalendar devolve as semanas do mês como listas de 7 números (0 = dia de outro mês).
    """
    semanas = calendar.monthcalendar(ano, 11)
    quintas = [s[calendar.THURSDAY] for s in semanas if s[calendar.THURSDAY] != 0]
    return date(ano, 11, quintas[3]) + timedelta(days=1)


eventos = []   # cada evento: (data, ícone, descrição)

# ── 1. RDAP: nascimento e alteração do domínio ────────────────────────────
rdap = json.loads((PASTA_CASO / "rdap_megaoferta.json").read_text(encoding="utf-8"))
nomes = {"registration": "Domínio registrado", "last changed": "Registro do domínio alterado"}
for e in rdap["events"]:
    if e["eventAction"] in nomes:
        quando = datetime.fromisoformat(e["eventDate"].replace("Z", "+00:00")).astimezone(FUSO)
        eventos.append((quando.date(), "🌐", f"{nomes[e['eventAction']]} (RDAP, {quando:%H:%M})"))

# ── 2. Wayback: capturas e o que o "length" revela ────────────────────────
cdx = json.loads((PASTA_CASO / "wayback_cdx_megaoferta.json").read_text(encoding="utf-8"))
cabecalho, *linhas = cdx                        # "desempacota": 1º item no cabeçalho, o resto em linhas
capturas = [dict(zip(cabecalho, l)) for l in linhas]
tamanho_anterior = None
for c in capturas:
    quando = datetime.strptime(c["timestamp"], "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc).astimezone(FUSO)
    tamanho = int(c["length"])
    nota = f"captura Wayback · HTTP {c['statuscode']} · {tamanho} bytes"
    if c["statuscode"] == "404":
        nota += " → 🚩 SITE FORA DO AR"
    elif tamanho_anterior and tamanho < tamanho_anterior * 0.3:
        # Encolheu mais de 70%: a vitrine com produtos virou uma página quase vazia.
        nota += f" → 🚩 encolheu {1 - tamanho / tamanho_anterior:.0%} (página de 'manutenção'?)"
    eventos.append((quando.date(), "📸", nota))
    tamanho_anterior = tamanho

# ── 3. Denúncias: primeira, última e picos ────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    datas = [date.fromisoformat(l["data"]) for l in csv.DictReader(arquivo, delimiter=";")]
por_dia = Counter(datas)
eventos.append((min(datas), "📨", "Primeira denúncia"))
eventos.append((max(datas), "📨", "Última denúncia"))
for dia, qtd in por_dia.items():
    if qtd >= 4:
        eventos.append((dia, "📈", f"Pico: {qtd} denúncias num só dia"))

# ── 4. Black Friday ───────────────────────────────────────────────────────
bf = black_friday(2025)
eventos.append((bf, "🛒", "BLACK FRIDAY 2025"))

# ── 5. Imprimir a linha do tempo ordenada ─────────────────────────────────
# sorted() em tuplas compara a data primeiro; em empate, o ícone (só para ficar estável).
print("🗓️ LINHA DO TEMPO — Operação Vitrine Fantasma\n")
criacao = min(d for d, i, _ in eventos if i == "🌐")
for dia, icone, texto in sorted(eventos):
    print(f"   {dia:%d/%m/%Y} {DIAS_SEMANA[dia.weekday()]}  D+{(dia - criacao).days:<3} {icone} {texto}")

# ── 6. O efeito Black Friday ──────────────────────────────────────────────
perto = sum(q for d, q in por_dia.items() if abs((d - bf).days) <= JANELA_DIAS)
dias_janela = 2 * JANELA_DIAS + 1
periodo = (max(datas) - min(datas)).days + 1
print(f"\n🛒 Black Friday 2025: {bf:%d/%m/%Y} (sexta após a 4ª quinta de novembro)")
print(f"   {perto} de {len(datas)} denúncias ({perto / len(datas):.0%}) caíram entre "
      f"{bf - timedelta(JANELA_DIAS):%d/%m} e {bf + timedelta(JANELA_DIAS):%d/%m}: "
      f"{dias_janela} dias de um período de {periodo}.")
media_geral = len(datas) / periodo
media_janela = perto / dias_janela
print(f"   Média: {media_janela:.1f} denúncias/dia na janela × {media_geral:.1f}/dia no período todo "
      f"({media_janela / media_geral:.1f}x).")
print("\n💡 Leitura: o golpe nasceu 10 dias antes da 1ª vítima, acelerou na semana da Black Friday,")
print("   virou 'manutenção' em 01/12 e saiu do ar em 05/12. Roteiro clássico de loja falsa sazonal.")
