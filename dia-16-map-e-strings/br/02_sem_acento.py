"""
Sem acento, sem maiúscula: a "chave de comparação" que junta grafias diferentes.

Carta 37 (rank A) — Jutsu dos Muitos Nomes (parte 2)

O que você aprende:
  • a tirar acentos com unicodedata (NFKD): "Kauã Brandão" → "kaua brandao";
  • a diferença entre lower() e casefold();
  • a combinar map() (transformar tudo) com filter() (ficar só com o que interessa).

Como rodar (dentro da pasta dia-16-map-e-strings):
    python br/02_sem_acento.py
"""

import csv
import json
import unicodedata          # tabela oficial Unicode: sabe que "ã" = "a" + "~"
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
PROCURAR = "brandao"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"


def sem_acento(texto):
    """Remove acentos e cedilha, mantendo as letras base.

    NFKD separa cada letra acentuada em duas peças: a letra e o acento.
    Depois jogamos fora as peças que são "marcas combinantes" (os acentos).
    """
    decomposto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in decomposto if not unicodedata.combining(c))


def chave(texto):
    """Chave de comparação: sem acento, minúscula 'agressiva' e espaços arrumados."""
    # casefold() é um lower() mais forte, pensado para comparar textos
    # (ex.: o "ß" alemão vira "ss"). Para nomes BR dá o mesmo, mas é o hábito certo.
    return " ".join(sem_acento(texto).casefold().split())


# ── 1. Demonstração ───────────────────────────────────────────────────────
print("🧪 Antes → chave de comparação\n")
for exemplo in ["Kauã Teixeira Brandão", "KAUA T. BRANDAO", "Poços de Caldas", "Pocos de Caldas", "  São  João "]:
    print(f"   {exemplo!r:<26} → {chave(exemplo)!r}")

# ── 2. Os nomes do suspeito espalhados pelas evidências ───────────────────
# Cada fonte grafou o nome de um jeito. Coletamos de onde eles aparecem.
rdap = json.loads((PASTA_CASO / "rdap_megaoferta.json").read_text(encoding="utf-8"))
nome_rdap = next(c[3] for ent in rdap["entities"] for c in ent["vcardArray"][1] if c[0] == "fn")

nome_whois = ""
for linha in (PASTA_CASO / "whois_megaoferta.txt").read_text(encoding="utf-8").splitlines():
    if linha.startswith("owner:"):
        nome_whois = linha.split(":", 1)[1].strip()   # tudo depois do primeiro ":"

nome_painel = ""
for linha in (PASTA_CASO / "painel_dump.sql").read_text(encoding="utf-8").splitlines():
    if "Brandão" in linha and "contas_recebimento" in linha:
        nome_painel = linha.split("'")[1]             # o texto entre as primeiras aspas simples

fontes = {"RDAP": nome_rdap, "WHOIS": nome_whois, "dump do painel": nome_painel,
          "registro informado à polícia": "Kauã Teixeira Brandão"}

print("\n🕵️ O mesmo sobrenome em fontes diferentes:\n")
for fonte, nome in fontes.items():
    print(f"   {fonte:<30} {nome:<28} → {chave(nome)}")

# ── 3. map + filter nos nomes das vítimas ─────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    linhas = list(csv.DictReader(arquivo, delimiter=";"))

nomes = [l["nome_vitima"] for l in linhas]
chaves = list(map(chave, nomes))                             # transforma TODOS
alvo = chave(PROCURAR)
com_alvo = list(filter(lambda c: alvo in c, chaves))         # fica só com quem contém o alvo
# lambda é uma função de uma linha sem nome: "recebe c, devolve (alvo in c)".

print(f"\n🔎 Vítimas cujo nome contém '{alvo}': {len(com_alvo)}")
print("   (Zero é a resposta esperada: o sobrenome do suspeito não aparece entre as vítimas.)")

# ── 4. Bônus: cidades digitadas de jeitos diferentes ──────────────────────
cidades = [l["cidade"] for l in linhas]
print(f"\n🏙️ Cidades como as vítimas digitaram: {len(set(cidades))} grafias diferentes")
print(f"🏙️ Depois da chave sem acento:       {len(set(map(chave, cidades)))} grafias diferentes")
print("   (Os erros de digitação, como 'Belo Horizone', continuam: isso é trabalho do Dia 7, com difflib.)")
