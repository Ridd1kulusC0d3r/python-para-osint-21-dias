"""
Olá, NFA: o seu primeiro script com nome, emoji e a hora certa de Brasília.

Carta 22 (rank B) — Jutsu do Primeiro Alerta

O que você aprende:
  • print() com vários pedaços, com sep= e com end=;
  • f-strings: colocar o valor de uma variável dentro do texto com {chaves};
  • que emoji também é texto (é só mais um caractere Unicode);
  • a pegar a data e a hora no fuso America/Sao_Paulo, com plano B se o fuso faltar.

Como rodar (dentro da pasta dia-01-primeiro-script):
    python br/01_ola_nfa.py
"""

from datetime import datetime, timedelta, timezone  # tudo o que precisamos para datas e fusos

# ── Parâmetros (no Colab viram um formulário) ─────────────────────────────
# Troque o valor entre aspas e rode de novo. É assim que se "personaliza" um script.
MEU_NOME = "Analista"  #@param {type:"string"}
UNIDADE = "Núcleo de Fontes Abertas (NFA)"  #@param {type:"string"}

# ── 1. O print mais simples ───────────────────────────────────────────────
# Igual ao do cipher387: um texto entre aspas dentro de print().
print("Bem-vindo(a) ao curso de 21 dias de Python para OSINT!")

# ── 2. Vários pedaços no mesmo print ──────────────────────────────────────
# Separados por vírgula, o print junta os pedaços com um espaço no meio.
print("Unidade:", UNIDADE)
# sep= troca o separador; aqui usamos " · " em vez do espaço.
print("Belo Horizonte", "MG", "Brasil", sep=" · ")

# ── 3. f-string: o jeito moderno de montar textos ─────────────────────────
# O "f" antes das aspas avisa: "procure {variáveis} aqui dentro e troque pelo valor".
print(f"👋 Olá, {MEU_NOME}! Seu crachá do {UNIDADE} está ativo.")

# Dentro das chaves pode ir uma conta ou uma função, não só o nome da variável.
print(f"🔠 Seu nome tem {len(MEU_NOME)} letras e, em maiúsculas, fica {MEU_NOME.upper()}.")

# ── 4. Emojis são texto ───────────────────────────────────────────────────
# Cada emoji é um caractere como qualquer letra. Dá para repetir texto com *.
print("🚨" * 3, "ALERTA DE GOLPE", "🚨" * 3)
# end= muda o que o print coloca no final (o padrão é pular linha, "\n").
print("Carregando", end="")
print("...", end="")
print(" pronto! ✅")

# ── 5. Data e hora de Brasília ────────────────────────────────────────────
# Em investigação, horário SEMPRE com fuso. "14h" sem fuso não serve como registro.
# zoneinfo (Python 3.9+) conhece os fusos do mundo todo. No Windows, pode faltar o
# banco de fusos (pacote tzdata): nesse caso usamos UTC-3 fixo, que vale para Brasília
# desde 2019, quando o horário de verão foi extinto.
try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))

agora = datetime.now(FUSO)

# strftime transforma a data em texto, no formato que quisermos:
#   %d = dia, %m = mês, %Y = ano com 4 dígitos, %H:%M:%S = hora:minuto:segundo
print(f"\n🕒 Agora em Brasília: {agora:%d/%m/%Y %H:%M:%S}")
# isoformat() é o formato internacional (bom para registros e planilhas).
print(f"🗂️  Formato ISO 8601:  {agora.isoformat(timespec='seconds')}")

# Os dias da semana em português, sem depender da configuração do computador.
DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
        "sexta-feira", "sábado", "domingo"]
# weekday() devolve 0 para segunda, 1 para terça... e 6 para domingo.
print(f"📅 Hoje é {DIAS[agora.weekday()]}.")

print("\n✅ Seu primeiro script rodou. Carta 22 conquistada!")
