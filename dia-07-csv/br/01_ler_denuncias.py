"""
Ler a planilha de denúncias (CSV com ";") e somar o prejuízo sem errar centavos.

Carta 28 (rank B) — Jutsu da Planilha Viva

O que você aprende:
  • csv.DictReader: cada linha vira um dicionário {"coluna": "valor"};
  • delimiter=";" (padrão das planilhas brasileiras) e encoding="utf-8";
  • por que somar dinheiro com Decimal e não com float;
  • a agrupar valores por produto com um dicionário.

Como rodar (dentro da pasta dia-07-csv):
    python br/01_ler_denuncias.py
"""

import csv
from collections import defaultdict   # dicionário que cria o valor inicial sozinho
from decimal import Decimal           # números decimais exatos (dinheiro!)
from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"


def reais(valor):
    """Decimal('54877.40') → 'R$ 54.877,40' (formato brasileiro, sem depender de locale)."""
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ── 1. Abrir e ler ────────────────────────────────────────────────────────
# newline="" é a recomendação oficial do módulo csv (evita problemas com quebras de linha).
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8", newline="") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=";")
    colunas = leitor.fieldnames          # a primeira linha vira os nomes das colunas
    denuncias = list(leitor)             # list() lê todas as linhas de uma vez

print(f"📄 {len(denuncias)} denúncias · colunas: {', '.join(colunas)}\n")
print(f"🔎 Primeira linha como dicionário:\n   {dict(denuncias[0])}\n")

# ── 2. A armadilha do float ───────────────────────────────────────────────
# O computador guarda float em binário e alguns centavos "escorregam".
soma_float = sum(float(d["valor"]) for d in denuncias)
soma_decimal = sum(Decimal(d["valor"]) for d in denuncias)   # "149.90" vira Decimal exato
print(f"🧮 Soma com float:   {soma_float!r}")
print(f"🧮 Soma com Decimal: {soma_decimal!r}   ← use este para dinheiro")
# Aqui o float até acertou (por sorte do arredondamento na hora de imprimir), mas veja:
print(f"   Prova do problema: 0.1 + 0.2 com float = {0.1 + 0.2!r}; com Decimal = {Decimal('0.1') + Decimal('0.2')!r}\n")

# ── 3. Total e quantidade por produto ─────────────────────────────────────
total_produto = defaultdict(Decimal)    # valor inicial: Decimal('0')
qtd_produto = defaultdict(int)          # valor inicial: 0
for d in denuncias:
    total_produto[d["produto"]] += Decimal(d["valor"])
    qtd_produto[d["produto"]] += 1

print("📦 Prejuízo por produto (do maior para o menor):")
# sorted com key: ordena pelos valores; reverse=True = do maior para o menor
for produto, total in sorted(total_produto.items(), key=lambda par: par[1], reverse=True):
    print(f"   {produto:<18} {qtd_produto[produto]:>2} vítima(s)  {reais(total):>14}")
print(f"   {'TOTAL':<18} {len(denuncias):>2} vítima(s)  {reais(soma_decimal):>14}")

# ── 4. Uma pergunta rápida: quantas denúncias por chave PIX? ──────────────
por_chave = defaultdict(int)
for d in denuncias:
    por_chave[d["chave_pix_destino"]] += 1
print("\n🔑 Denúncias por chave PIX de destino:")
for chave, qtd in sorted(por_chave.items(), key=lambda par: -par[1]):
    print(f"   {chave}  {qtd:>2}")
