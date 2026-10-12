"""
Gerador de variantes de username: os muitos nomes de Kau.

Carta 37 (rank A) — Jutsu dos Muitos Nomes (parte 3)

O que você aprende:
  • a montar usernames prováveis a partir de um nome completo e de um apelido;
  • separadores (. _ -), iniciais, sufixos numéricos e "leetspeak" simples;
  • a usar set() para não repetir e sorted() para ordenar;
  • a salvar a lista num arquivo para alimentar ferramentas como blackbird/maigret (Dia 3).

Como rodar (dentro da pasta dia-16-map-e-strings):
    python br/03_variantes_username.py
"""

import unicodedata
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
NOME_COMPLETO = "Kauã Teixeira Brandão"  #@param {type:"string"}
APELIDO = "kau.ofertas"  #@param {type:"string"}
SUFIXOS = "1, 01, 2025, 31, br, oficial"  #@param {type:"string"}
USAR_LEET = True  #@param {type:"boolean"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
SAIDAS = PASTA_DIA / "saidas"

SEPARADORES = ["", ".", "_", "-"]
# Leetspeak "leve": só as trocas mais comuns. Mais que isso explode a lista.
LEET = str.maketrans({"a": "4", "e": "3", "o": "0", "i": "1"})
PARTICULAS = {"da", "de", "do", "das", "dos", "e"}


def limpar(texto):
    """Sem acento, minúsculo e só letras/números (usernames não aceitam 'ã')."""
    sem = "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))
    return "".join(c for c in sem.lower() if c.isalnum())


# ── 1. Quebrar o nome em partes úteis ─────────────────────────────────────
partes = [limpar(p) for p in NOME_COMPLETO.split() if p.lower() not in PARTICULAS]
primeiro, ultimo = partes[0], partes[-1]           # "kaua", "brandao"
meio = partes[1:-1]                                # ["teixeira"]
print(f"🧩 Partes do nome: {partes}")

# ── 2. Combinações "base" (sem separador ainda) ───────────────────────────
# Cada item é uma lista de pedaços; o separador entra depois.
bases = [
    [primeiro, ultimo],                    # kaua brandao
    [ultimo, primeiro],                    # brandao kaua
    [primeiro[0], ultimo],                 # k brandao
    [primeiro, ultimo[0]],                 # kaua b
    [primeiro] + meio + [ultimo],          # kaua teixeira brandao
    ["".join(p[0] for p in partes)],       # ktb (as iniciais: lembra do handle KTB123 do RDAP?)
    [primeiro[:3], ultimo],                # kau brandao
]

# ── 3. O apelido já conhecido também gera variantes ───────────────────────
# "kau.ofertas" → pedaços ["kau", "ofertas"]: trocamos o separador.
pedacos_apelido = [p for p in APELIDO.replace("_", ".").replace("-", ".").split(".") if p]
bases.append(pedacos_apelido)
bases.append(list(reversed(pedacos_apelido)))      # ofertas.kau

# ── 4. Aplicar separadores ────────────────────────────────────────────────
variantes = set()                                  # set: repetidos somem sozinhos
for pedacos in bases:
    for sep in SEPARADORES:
        variantes.add(sep.join(pedacos))

# ── 5. Sufixos numéricos e leetspeak ──────────────────────────────────────
sufixos = [s.strip() for s in SUFIXOS.split(",") if s.strip()]
for v in list(variantes):                          # list(): congelamos antes de mexer no set
    for s in sufixos:
        variantes.add(v + s)
        variantes.add(f"{v}_{s}")
    if USAR_LEET:
        variantes.add(v.translate(LEET))           # "kau.ofertas" → "k4u.0f3rt4s"

# Usernames de 1 ou 2 letras não servem para nada: filtramos.
variantes = {v for v in variantes if len(v) >= 3}

# ── 6. Ordenar: primeiro as "limpas" (sem números), depois as mais curtas, depois A→Z
# A key devolve uma tupla; o Python compara o 1º item, depois o 2º, e assim por diante.
# any(c.isdigit() for c in v) é False (=0) para "kaua.brandao" e True (=1) para "kaua1".
ordenadas = sorted(variantes, key=lambda v: (any(c.isdigit() for c in v), len(v), v))
print(f"\n🧮 {len(ordenadas)} variantes geradas. As 20 primeiras:\n")
for v in ordenadas[:20]:
    print(f"   {v}")

# ── 7. Salvar (um por linha: formato que ferramentas de username aceitam) ─
SAIDAS.mkdir(exist_ok=True)
destino = SAIDAS / "variantes_username.txt"
destino.write_text("\n".join(ordenadas) + "\n", encoding="utf-8")
print(f"\n💾 Lista completa em {destino.relative_to(PASTA_DIA)}")
print("⚠️ Variante NÃO é identidade: cada conta encontrada precisa ser confirmada por outros vínculos.")
