"""
Caso Vitrine Fantasma: quem recebeu o dinheiro? (JOIN + GROUP BY)

Carta 29 (rank B) — Jutsu do Arquivo Morto (aplicação no caso)

O que você aprende:
  • JOIN: juntar duas tabelas pelo campo em comum (pedidos.conta_id = contas_recebimento.id);
  • GROUP BY + COUNT/SUM/MIN/MAX: resumir por conta laranja;
  • por que o REAL do SQLite tem o mesmo problema do float (e como contornar);
  • a cruzar o dump com a planilha de denúncias: as fontes concordam?

Como rodar (dentro da pasta dia-08-bancos-de-dados):
    python br/02_quem_recebeu.py
"""

import csv
import sqlite3
from decimal import Decimal
from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"


def reais(valor):
    """Decimal → 'R$ 21.242,10'."""
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


banco = sqlite3.connect(":memory:")
banco.executescript((PASTA_CASO / "painel_dump.sql").read_text(encoding="utf-8"))

# ── 1. A consulta principal ───────────────────────────────────────────────
# Leia de baixo para cima: pegue os pedidos (p), junte com a conta (c) cujo id
# é igual ao conta_id do pedido, agrupe por conta e calcule os totais de cada grupo.
# ROUND(valor * 100) transforma reais em CENTAVOS inteiros: soma de inteiros não erra.
CONSULTA = """
    SELECT c.titular,
           c.banco,
           c.chave_pix,
           COUNT(*)                            AS pedidos,
           SUM(CAST(ROUND(p.valor * 100) AS INTEGER)) AS centavos,
           MIN(p.data)                         AS primeiro,
           MAX(p.data)                         AS ultimo
      FROM pedidos AS p
      JOIN contas_recebimento AS c ON c.id = p.conta_id
     GROUP BY c.id
     ORDER BY centavos DESC
"""

print("💸 Dinheiro recebido por conta (dump do painel):\n")
total_dump = Decimal("0")
for titular, banco_nome, chave, pedidos, centavos, primeiro, ultimo in banco.execute(CONSULTA):
    valor = Decimal(centavos) / 100                  # centavos → reais, sem erro
    total_dump += valor
    print(f"👤 {titular}  ({banco_nome})")
    print(f"   chave {chave}")
    print(f"   {pedidos} pedidos · {reais(valor)} · de {primeiro} a {ultimo}\n")
print(f"🧮 Total no dump: {reais(total_dump)}")

# ── 2. Por que não SUM(valor) direto? ─────────────────────────────────────
bruto = banco.execute("SELECT SUM(valor) FROM pedidos WHERE conta_id = 1").fetchone()[0]
print(f"\n💡 SUM(valor) direto na conta 1 dá {bruto!r}: o REAL do SQLite é float. Centavos, sempre.")

# ── 3. Conferir com a planilha das vítimas ────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8", newline="") as arquivo:
    denuncias = list(csv.DictReader(arquivo, delimiter=";"))
total_planilha = sum(Decimal(d["valor"]) for d in denuncias)
print(f"\n📄 Total na planilha de denúncias: {reais(total_planilha)}")
if total_planilha == total_dump:
    print("✅ O painel da loja e as vítimas contam a MESMA história, real por real.")
else:
    print(f"🚩 Diferença de {reais(abs(total_planilha - total_dump))}: há vítimas que não denunciaram (ou vice-versa).")

# ── 4. Pergunta de investigador: algum titular aparece nos dois lados? ────
# O vendedor que assina "Kau" aparece nos registros como Kauã Teixeira Brandão (caso/README.md).
suspeitas = banco.execute(
    "SELECT titular FROM contas_recebimento WHERE titular LIKE ?", ("%Brandão%",)).fetchall()
for (titular,) in suspeitas:
    print(f"\n🔎 '{titular}' tem o mesmo sobrenome do vendedor 'Kau'. Coincidência ou empresa de fachada?")
    print("   Anote como hipótese, não como conclusão: sobrenome igual não prova vínculo.")
banco.close()
