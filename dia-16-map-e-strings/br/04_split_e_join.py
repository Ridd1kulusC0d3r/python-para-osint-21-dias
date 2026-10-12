"""
split, join e strip na prática: desmontar uma conversa exportada do WhatsApp.

Carta 37 (rank A) — Jutsu dos Muitos Nomes (parte 4)

O que você aprende:
  • a quebrar a linha "[28/11/2025 21:14] Kau Ofertas: mensagem" em data, hora, autor e texto;
  • a usar split com limite (maxsplit) para não cortar o ":" que aparece dentro da mensagem;
  • a limpar espaços com strip() e a remontar textos com join().

Como rodar (dentro da pasta dia-16-map-e-strings):
    python br/04_split_e_join.py
"""

import csv
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
AUTOR_FOCO = "Kau Ofertas"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"


def desmontar(linha):
    """'[28/11/2025 21:14] Kau Ofertas: Boa noite!' → dict com data, hora, autor, mensagem.

    Devolve None se a linha não estiver no formato esperado.
    """
    linha = linha.strip()                       # tira espaços e o "\n" das pontas
    if not linha.startswith("["):
        return None
    # 1. Separar o carimbo "[...]" do resto. split("]", 1) corta só no PRIMEIRO "]".
    carimbo, resto = linha[1:].split("]", 1)    # "28/11/2025 21:14" e " Kau Ofertas: Boa noite!"
    data, hora = carimbo.split()                # split() sem argumento: corta no espaço
    # 2. Autor e mensagem. maxsplit=1 é essencial: a mensagem pode ter ":"
    #    (ex.: "Chave PIX: f38b..."), e não queremos cortar ali.
    if ":" not in resto:
        return None
    autor, mensagem = resto.split(":", 1)
    return {"data": data, "hora": hora, "autor": autor.strip(), "mensagem": mensagem.strip()}


# ── 1. Um exemplo comentado ───────────────────────────────────────────────
exemplo = "[28/11/2025 21:16] Kau Ofertas: Chave PIX: f38b2ffc-80a4-df5a-51c9-bc701e7ea419"
# Armadilha 1: a hora "21:16" também tem ":". Por isso primeiro tiramos o carimbo "[...]".
resto = exemplo.split("]", 1)[1]
print(f"✂️  Depois do ']':          {resto!r}")
print("🔪 split(':') sem limite corta demais:")
print(f"   {resto.split(':')}")
print("✅ split(':', 1) corta só uma vez (autor | mensagem):")
print(f"   {resto.split(':', 1)}")
print(f"\n🧩 desmontar() →  {desmontar(exemplo)}")

# ── 2. A conversa inteira ─────────────────────────────────────────────────
texto = (PASTA_CASO / "conversa_whatsapp.txt").read_text(encoding="utf-8")
mensagens = [m for m in map(desmontar, texto.splitlines()) if m]   # map + descarta os None
print(f"\n💬 {len(mensagens)} mensagens lidas.")

# ── 3. Quem falou quanto? ─────────────────────────────────────────────────
contagem = {}
for m in mensagens:
    contagem[m["autor"]] = contagem.get(m["autor"], 0) + 1
for autor, total in contagem.items():
    print(f"   {autor:<14} {'▇' * total} {total}")

# ── 4. Só as falas do autor em foco, remontadas com join ──────────────────
falas = [f"{m['data']} {m['hora']} — {m['mensagem']}" for m in mensagens if m["autor"] == AUTOR_FOCO]
print(f"\n🗣️ Falas de {AUTOR_FOCO}:\n")
print("\n".join(f"   {f}" for f in falas))

# Palavras mais longas que ele usa: split() quebra a frase em palavras;
# strip(".,!?") tira a pontuação colada nas pontas de cada uma.
palavras = {p.strip(".,!?🔥").lower() for m in mensagens if m["autor"] == AUTOR_FOCO
            for p in m["mensagem"].split()}
print(f"\n🔤 Vocabulário de {AUTOR_FOCO}: {len(palavras)} palavras diferentes.")

# ── 5. Salvar como CSV (agora dá para abrir numa planilha) ────────────────
SAIDAS.mkdir(exist_ok=True)
with open(SAIDAS / "conversa_estruturada.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=["data", "hora", "autor", "mensagem"], delimiter=";")
    escritor.writeheader()
    escritor.writerows(mensagens)
print("💾 saidas/conversa_estruturada.csv gravado.")
