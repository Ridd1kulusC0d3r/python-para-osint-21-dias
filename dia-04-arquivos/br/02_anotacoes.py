"""
Caderno de anotações do analista: acrescentar notas com carimbo de data/hora.

Carta 25 (rank B) — Jutsu dos Depoimentos (parte 2)

O que você aprende:
  • a diferença entre os modos "w" (apaga e escreve), "a" (acrescenta) e "x" (só cria se não existir);
  • a escrever várias linhas com write() e writelines() (e por que nenhum dos dois pula linha sozinho);
  • a carimbar cada nota com data/hora de Brasília (ISO 8601 com fuso);
  • a armadilha do Windows: sem encoding="utf-8", o Python usa cp1252 e os acentos viram lixo.

Como rodar (dentro da pasta dia-04-arquivos):
    python br/02_anotacoes.py          # rode duas vezes e veja o caderno crescer
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
NOTA = "DEN-003 e DEN-001 pagaram na mesma chave PIX (f38b2ffc…). Pedir extrato ao banco."  #@param {type:"string"}
ANALISTA = "Analista"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
SAIDAS = PASTA_DIA / "saidas"
SAIDAS.mkdir(exist_ok=True)               # cria a pasta se ela ainda não existir
CADERNO = SAIDAS / "caderno_do_analista.txt"

try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:                          # Windows sem tzdata: UTC-3 fixo
    FUSO = timezone(timedelta(hours=-3))

# ── 1. Modo "x": criar o cabeçalho só na PRIMEIRA vez ─────────────────────
# "x" dá erro (FileExistsError) se o arquivo já existe. Usamos isso a nosso favor:
# o cabeçalho é escrito uma única vez, nunca duplicado.
try:
    with open(CADERNO, "x", encoding="utf-8") as caderno:
        caderno.write("CADERNO DO ANALISTA — Operação Vitrine Fantasma\n")
        caderno.write("Formato: data/hora ISO 8601 (Brasília) | analista | nota\n")
        caderno.write("=" * 60 + "\n")
    print(f"🆕 Caderno criado: {CADERNO.relative_to(PASTA_DIA)}")
except FileExistsError:
    print(f"📓 Caderno já existe: {CADERNO.relative_to(PASTA_DIA)} (vamos acrescentar)")

# ── 2. Modo "a": acrescentar a nota de hoje, sem apagar as antigas ────────
agora = datetime.now(FUSO).isoformat(timespec="seconds")       # ex.: 2026-10-12T09:15:02-03:00
with open(CADERNO, "a", encoding="utf-8") as caderno:
    # write() NÃO pula linha: o "\n" no fim é obrigatório, senão as notas grudam.
    caderno.write(f"{agora} | {ANALISTA} | {NOTA}\n")
    # writelines() grava uma lista de textos de uma vez (também sem pular linha sozinho).
    caderno.writelines([
        f"{agora} | {ANALISTA} | Lidos 5 depoimentos; 'Kau' citado em todos.\n",
        f"{agora} | {ANALISTA} | Próximo passo: extrair contatos e chaves PIX (br/03).\n",
    ])
print(f"✍️  3 notas acrescentadas às {agora}")

# ── 3. Reler o caderno ────────────────────────────────────────────────────
with open(CADERNO, encoding="utf-8") as caderno:
    conteudo = caderno.readlines()
notas = [l for l in conteudo if " | " in l and l[:4].isdigit()]   # só as linhas que são notas
print(f"\n📚 O caderno tem {len(notas)} notas. As três últimas:")
for linha in notas[-3:]:
    print("   " + linha.rstrip("\n"))

# ── 4. Modo "w": cuidado, ele APAGA tudo ──────────────────────────────────
rascunho = SAIDAS / "rascunho.txt"
with open(rascunho, "w", encoding="utf-8") as r:
    r.write("primeira versão\n")
with open(rascunho, "w", encoding="utf-8") as r:            # abrir de novo com "w"...
    r.write("segunda versão\n")
print(f"\n⚠️  Modo 'w' duas vezes: o rascunho só tem {rascunho.read_text(encoding='utf-8').strip()!r}.")
print("   Para registro de investigação, use 'a': nada some, tudo fica em ordem cronológica.")

# ── 5. A armadilha do cp1252 (Windows) ────────────────────────────────────
# No Windows em português, sem encoding=, o Python (até a versão 3.14) usa cp1252.
# Simulamos aqui o que acontece quando alguém grava em UTF-8 e outro lê como cp1252.
original = "Vítima de Divinópolis pagou R$ 149,90 — chave PIX"
bytes_utf8 = original.encode("utf-8")                        # como fica gravado no disco
lido_errado = bytes_utf8.decode("cp1252", errors="replace")  # como o Windows "antigo" leria
print("\n🪤 A armadilha da codificação")
print(f"   Gravado em UTF-8 : {original}")
print(f"   Lido como cp1252 : {lido_errado}")
print("   Moral: SEMPRE encoding='utf-8' ao gravar E ao ler.")
