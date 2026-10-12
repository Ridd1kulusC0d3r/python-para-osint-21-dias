"""
Gráfico de barras no terminal: vítimas por cidade (já padronizada).

Carta 39 (rank A) — Jutsu do Mapa das Vítimas

O que você aprende:
  • a padronizar cidades digitadas de jeitos diferentes (revisão do Dia 7);
  • a desenhar barras com o caractere ▇, proporcionais ao maior valor;
  • a usar Counter.most_common() para ordenar do maior para o menor.

Como rodar (dentro da pasta dia-18-graficos-e-mapas):
    python br/01_grafico_terminal.py
"""

import csv
import difflib                       # acha a palavra "mais parecida" (corrige 'Belo Horizone')
import unicodedata
from collections import Counter
from decimal import Decimal
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
LARGURA_MAXIMA = 40  #@param {type:"integer"}
MEDIDA = "vitimas"  #@param ["vitimas", "prejuizo"]

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"

# Nomes oficiais (como no IBGE) das cidades que aparecem no caso.
OFICIAIS = ["Belo Horizonte", "Betim", "Contagem", "Divinópolis", "Governador Valadares",
            "Ipatinga", "Juiz de Fora", "Poços de Caldas", "Sete Lagoas", "Uberaba", "Uberlândia"]
APELIDOS = {"bh": "Belo Horizonte", "bhz": "Belo Horizonte", "gv": "Governador Valadares", "jf": "Juiz de Fora"}


def chave(texto):
    sem = "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))
    return " ".join(sem.casefold().split())


CHAVES_OFICIAIS = {chave(c): c for c in OFICIAIS}


def padronizar(cidade):
    """'belo horizone' → 'Belo Horizonte' (apelido, depois igualdade, depois o mais parecido)."""
    k = chave(cidade)
    if k in APELIDOS:
        return APELIDOS[k]
    if k in CHAVES_OFICIAIS:
        return CHAVES_OFICIAIS[k]
    parecidas = difflib.get_close_matches(k, CHAVES_OFICIAIS, n=1, cutoff=0.8)
    return CHAVES_OFICIAIS[parecidas[0]] if parecidas else cidade


# ── 1. Contar ─────────────────────────────────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    denuncias = list(csv.DictReader(arquivo, delimiter=";"))

contagem = Counter()
for d in denuncias:
    cidade = padronizar(d["cidade"])
    # Counter soma o que você mandar: 1 por vítima, ou o valor em reais.
    contagem[cidade] += 1 if MEDIDA == "vitimas" else Decimal(d["valor"])

# ── 2. Desenhar ───────────────────────────────────────────────────────────
maior = max(contagem.values())
titulo = "Vítimas por cidade" if MEDIDA == "vitimas" else "Prejuízo por cidade (R$)"
print(f"📊 {titulo} — {len(denuncias)} denúncias, {len(contagem)} cidades\n")

for cidade, valor in contagem.most_common():
    # Regra de três: o maior valor ganha LARGURA_MAXIMA blocos, os outros proporcionalmente.
    blocos = round(valor / maior * LARGURA_MAXIMA)
    rotulo = f"{valor}" if MEDIDA == "vitimas" else f"{valor:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")
    # :<22 = alinha à esquerda em 22 colunas; max(blocos, 1) garante pelo menos um bloquinho
    print(f"{cidade:<22} {'▇' * max(blocos, 1)} {rotulo}")

# ── 3. Uma leitura analítica ──────────────────────────────────────────────
rmbh = {"Belo Horizonte", "Contagem", "Betim"}       # Região Metropolitana de BH (parte dela)
na_rmbh = sum(v for c, v in contagem.items() if c in rmbh)
print(f"\n🧭 Grande BH (BH + Contagem + Betim): {na_rmbh} de {sum(contagem.values())} "
      f"({na_rmbh / sum(contagem.values()):.0%}). O resto está espalhado pelo interior de MG.")
print("💡 Golpe espalhado por várias regiões sugere divulgação online ampla (anúncio pago, grupos), não boca a boca local.")
