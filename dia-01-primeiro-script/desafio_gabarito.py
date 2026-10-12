"""
Gabarito do Desafio S do Dia 1 — Boletim de plantão.

Monta uma mensagem curta de plantão (do tipo que se cola no grupo da equipe) com:
carimbo de data/hora de Brasília, quantos dias se passaram desde a primeira denúncia,
o prejuízo em formato brasileiro (R$ 54.877,40) e a média por vítima.
Não usa internet.
"""

from datetime import date, datetime, timedelta, timezone

ANALISTA = "Analista"  #@param {type:"string"}
TOTAL_DENUNCIAS = 37  #@param {type:"integer"}
PREJUIZO_TOTAL = 54877.40  #@param {type:"number"}
PRIMEIRA_DENUNCIA = "2025-10-12"  #@param {type:"string"}

# Fuso de Brasília com plano B (Windows sem tzdata).
try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))

agora = datetime.now(FUSO)

# date.fromisoformat entende "AAAA-MM-DD". Subtrair duas datas dá um "timedelta";
# .days é o número de dias inteiros entre elas.
primeira = date.fromisoformat(PRIMEIRA_DENUNCIA)
dias_desde = (agora.date() - primeira).days

# Formato brasileiro: primeiro formatamos no padrão americano (vírgula no milhar,
# ponto no decimal) e depois trocamos os dois símbolos de lugar usando um "coringa".
americano = f"{PREJUIZO_TOTAL:,.2f}"
prejuizo_br = americano.replace(",", "§").replace(".", ",").replace("§", ".")
media = PREJUIZO_TOTAL / TOTAL_DENUNCIAS
media_br = f"{media:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")

boletim = f"""🚨 *BOLETIM DE PLANTÃO · NFA*
🕒 {agora:%d/%m/%Y %H:%M} (Brasília)
👤 {ANALISTA}

📨 Operação Vitrine Fantasma: {TOTAL_DENUNCIAS} denúncias
💸 Prejuízo: R$ {prejuizo_br} (média de R$ {media_br} por vítima)
⏳ Primeira denúncia há {dias_desde} dias ({primeira:%d/%m/%Y})
"""

print(boletim)
print(f"📏 Tamanho da mensagem: {len(boletim)} caracteres")
