"""
O mapa das vítimas: tirar repetidos, fazer ranking e comparar outubro x novembro.

Carta 34 (rank A) — Jutsu da Lista Ordenada (aplicação no caso)

O que você aprende:
  • a montar uma lista a partir de uma coluna do CSV;
  • dict.fromkeys(lista): tira repetidos MANTENDO a ordem em que apareceram;
  • set(lista): tira repetidos, mas sem ordem (e permite comparar grupos);
  • collections.Counter: conta quantas vezes cada item aparece (ranking);
  • operações de conjunto: & (nos dois), - (só em um), | (em algum).

Este script é 100% offline: lê caso/dados/denuncias.csv (fictício).

Como rodar (dentro da pasta dia-13-listas):
    python br/03_cidades_das_vitimas.py
"""

import csv
import unicodedata
from collections import Counter
from pathlib import Path

TOP = 5  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"

# Nomes oficiais (grafia do IBGE) das cidades que aparecem no caso.
# No Dia 7 você gerou essa lista automaticamente com a API do IBGE.
OFICIAIS = ["Belo Horizonte", "Betim", "Contagem", "Divinópolis", "Governador Valadares",
            "Ipatinga", "Juiz de Fora", "Poços de Caldas", "Sete Lagoas", "Uberaba", "Uberlândia"]
# Erros de digitação conhecidos (no Dia 7, o difflib descobriu isso sozinho).
CORRECOES = {"belo horizone": "belo horizonte"}


def sem_acento(texto):
    """'Poços de Caldas' → 'pocos de caldas' (mesma ideia do script 02)."""
    separado = unicodedata.normalize("NFKD", texto.strip())
    return "".join(c for c in separado if not unicodedata.combining(c)).casefold()


# Dicionário "chave sem acento → nome oficial", montado com uma compreensão de dicionário.
OFICIAL_POR_CHAVE = {sem_acento(nome): nome for nome in OFICIAIS}


def padronizar(cidade):
    chave = sem_acento(cidade)
    chave = CORRECOES.get(chave, chave)
    return OFICIAL_POR_CHAVE.get(chave, cidade)    # se não reconhecer, devolve como veio


# ── 1. Ler a coluna "cidade" (e o mês) ────────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    linhas = list(csv.DictReader(arquivo, delimiter=";"))

cidades_brutas = [linha["cidade"] for linha in linhas]
print(f"📨 {len(cidades_brutas)} denúncias.")

# ── 2. Repetidos: set x dict.fromkeys ─────────────────────────────────────
print(f"\n🔤 Grafias distintas (como as vítimas digitaram): {len(set(cidades_brutas))}")
for c in dict.fromkeys(cidades_brutas):          # ordem de aparição preservada
    print(f"   • {c}")

cidades = [padronizar(c) for c in cidades_brutas]   # compreensão de lista: aplica a função em todos
unicas = list(dict.fromkeys(cidades))
print(f"\n🏙️  Depois de padronizar: {len(unicas)} cidades (na ordem em que surgiram):")
print("   " + " · ".join(unicas))

# ── 3. Ranking com Counter ────────────────────────────────────────────────
contagem = Counter(cidades)
print(f"\n🏆 Top {TOP} cidades com mais vítimas:")
for posicao, (cidade, qtd) in enumerate(contagem.most_common(TOP), start=1):
    print(f"   {posicao}º {cidade:<22} {'█' * qtd} {qtd}")

# ── 4. Outubro x novembro com conjuntos ───────────────────────────────────
# A data vem como "2025-11-30": os 7 primeiros caracteres são "2025-11".
outubro = {padronizar(l["cidade"]) for l in linhas if l["data"].startswith("2025-10")}
novembro = {padronizar(l["cidade"]) for l in linhas if l["data"].startswith("2025-11")}

print("\n📅 Outubro x novembro:")
print(f"   Nos dois meses (&):      {sorted(outubro & novembro)}")
print(f"   Só em outubro (-):       {sorted(outubro - novembro)}")
print(f"   Só em novembro (-):      {sorted(novembro - outubro)}")
print(f"   Em algum mês (|):        {len(outubro | novembro)} cidades")

print("\n🧠 Leitura de analista: as cidades que só aparecem em novembro mostram o golpe")
print("   se espalhando pelo estado perto da Black Friday.")
