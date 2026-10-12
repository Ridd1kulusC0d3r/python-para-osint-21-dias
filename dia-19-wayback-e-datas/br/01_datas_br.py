"""
Datas e horas do jeito brasileiro: fuso, dd/mm/aaaa, timestamp Unix e dias da semana em português.

Carta 40 (rank A) — Jutsu da Linha do Tempo

O que você aprende:
  • a diferença entre data "ingênua" (sem fuso) e "consciente" (com fuso);
  • America/Sao_Paulo com zoneinfo (e o plano B para Windows sem tzdata);
  • strptime (texto → data) e strftime (data → texto) com dd/mm/aaaa;
  • timestamp Unix, timedelta e dias da semana em português SEM depender do locale;
  • por que o horário de verão importa em datas antigas (ele foi extinto em 2019).

Como rodar (dentro da pasta dia-19-wayback-e-datas):
    python br/01_datas_br.py
"""

from datetime import date, datetime, timedelta, timezone

# ── Parâmetros ────────────────────────────────────────────────────────────
DATA_TEXTO = "28/11/2025 21:14"  #@param {type:"string"}
DIAS_PARA_SOMAR = 30  #@param {type:"integer"}

# ── 1. O fuso de Brasília ─────────────────────────────────────────────────
# zoneinfo (Python 3.9+) usa a base oficial de fusos (IANA). No Windows essa base
# pode não existir: aí "pip install tzdata" resolve, ou usamos -03:00 fixo.
try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
    FUSO_COMPLETO = True
except Exception:
    FUSO = timezone(timedelta(hours=-3), "BRT")
    FUSO_COMPLETO = False
    print("⚠️ Base de fusos ausente: usando UTC-3 fixo (datas antes de 2019 podem errar 1 hora).")

# Dias e meses em português, na mão: strftime("%A") depende do "locale" do sistema,
# que no Colab e no GitHub Actions é inglês. Lista própria = mesmo resultado em qualquer lugar.
DIAS_SEMANA = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
               "sexta-feira", "sábado", "domingo"]           # weekday(): 0 = segunda
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def por_extenso(d):
    """date/datetime → 'sexta-feira, 28 de novembro de 2025'."""
    return f"{DIAS_SEMANA[d.weekday()]}, {d.day} de {MESES[d.month - 1]} de {d.year}"


# ── 2. Agora: ingênuo × consciente ────────────────────────────────────────
ingenua = datetime.now()                 # sem fuso: "hora do computador", seja ela qual for
consciente = datetime.now(FUSO)          # com fuso: sabe que é -03:00
utc = datetime.now(timezone.utc)
print("🕐 Agora")
print(f"   ingênua (sem fuso):     {ingenua:%d/%m/%Y %H:%M:%S}   tzinfo={ingenua.tzinfo}")
print(f"   Brasília (consciente):  {consciente:%d/%m/%Y %H:%M:%S} {consciente:%z}")
print(f"   UTC:                    {utc:%d/%m/%Y %H:%M:%S} {utc:%z}")
print(f"   📅 {por_extenso(consciente)}")
print("   💡 No Colab a 'ingênua' sai em UTC (3 h à frente). Em evidência, SEMPRE grave com fuso.")

# ── 3. Texto → data (strptime) e data → texto (strftime) ──────────────────
# %d dia · %m mês · %Y ano com 4 dígitos · %H hora 0–23 · %M minuto · %S segundo
momento = datetime.strptime(DATA_TEXTO, "%d/%m/%Y %H:%M").replace(tzinfo=FUSO)
print(f"\n🔤 '{DATA_TEXTO}' → {momento.isoformat()}")
print(f"   {por_extenso(momento)}, às {momento:%Hh%M}")
print(f"   Formato ISO 8601 (o melhor para ordenar e trocar dados): {momento:%Y-%m-%d}")

# ── 4. Timestamp Unix ─────────────────────────────────────────────────────
# Segundos desde 01/01/1970 00:00 UTC. Aparece em logs, metadados de foto, APIs, Discord...
ts = int(momento.timestamp())
print(f"\n⏱️ Timestamp Unix: {ts}")
print(f"   de volta:        {datetime.fromtimestamp(ts, FUSO):%d/%m/%Y %H:%M} (Brasília)")
print(f"   o mesmo instante {datetime.fromtimestamp(ts, timezone.utc):%d/%m/%Y %H:%M} (UTC)")
# Timestamps em MILISSEGUNDOS (13 dígitos) são comuns em JavaScript: divida por 1000.
print(f"   em milissegundos: {ts * 1000}  → datetime.fromtimestamp(ms / 1000, FUSO)")

# ── 5. Contas com datas (timedelta) ───────────────────────────────────────
depois = momento + timedelta(days=DIAS_PARA_SOMAR)
print(f"\n➕ {DIAS_PARA_SOMAR} dias depois: {por_extenso(depois)}")
inicio_caso = date(2025, 10, 2)          # criação do domínio (Dia 15)
print(f"➖ Do registro do domínio até {momento:%d/%m}: {(momento.date() - inicio_caso).days} dias")

# ── 6. Horário de verão: por que o fuso "de verdade" importa ──────────────
# O Brasil teve horário de verão até fevereiro de 2019 (extinto pelo Decreto nº 9.772/2019).
# Em dezembro de 2018 Brasília estava em -02:00, não -03:00.
antigo = datetime(2018, 12, 15, 12, 0, tzinfo=FUSO)
print(f"\n☀️ 15/12/2018 12:00 em Brasília tinha deslocamento {antigo:%z}"
      f"{'  ← horário de verão!' if FUSO_COMPLETO else '  (fuso fixo: não sabe do verão)'}")
print(f"   15/12/2025 12:00 em Brasília tem deslocamento {datetime(2025, 12, 15, 12, tzinfo=FUSO):%z}")
print("   💡 Ao analisar evidência antiga com fuso fixo -03:00, você pode errar a hora em 1 h.")
