"""
Gabarito do Desafio S do Dia 8 — Conciliação: painel da loja × denúncias.

Coloca o dump do painel e a planilha de denúncias no MESMO banco SQLite, liga
cada denúncia ao pedido correspondente (cliente + data + valor), confere se a
chave PIX informada pela vítima é a da conta que o painel registrou, aponta
divergências e monta a linha do tempo de entrada em uso de cada conta laranja.
Grava saidas/conciliacao.csv. 100% offline (dados fictícios de caso/dados/).
"""

import csv
import sqlite3
from decimal import Decimal
from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"


def reais(centavos):
    return "R$ " + f"{Decimal(centavos) / 100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


banco = sqlite3.connect(":memory:")
banco.executescript((PASTA_CASO / "painel_dump.sql").read_text(encoding="utf-8"))

# Tabela com as denúncias (sem CPF e telefone: não precisamos deles para conciliar)
banco.execute("""CREATE TABLE denuncias (id TEXT PRIMARY KEY, data TEXT, nome TEXT,
                 valor_centavos INTEGER, chave_pix TEXT)""")
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8", newline="") as f:
    banco.executemany("INSERT INTO denuncias VALUES (?, ?, ?, ?, ?)", [
        (d["id"], d["data"], d["nome_vitima"], int(Decimal(d["valor"]) * 100), d["chave_pix_destino"])
        for d in csv.DictReader(f, delimiter=";")])

# LEFT JOIN: toda denúncia aparece, mesmo sem pedido correspondente (aí os campos do pedido vêm NULL).
CONCILIA = """
SELECT d.id, d.data, d.nome, d.valor_centavos, d.chave_pix,
       p.id AS pedido, c.titular, c.chave_pix AS chave_painel
  FROM denuncias AS d
  LEFT JOIN pedidos AS p
         ON p.cliente = d.nome AND p.data = d.data
        AND CAST(ROUND(p.valor * 100) AS INTEGER) = d.valor_centavos
  LEFT JOIN contas_recebimento AS c ON c.id = p.conta_id
 ORDER BY d.id
"""
linhas, problemas = [], 0
for den, data, nome, centavos, chave_vitima, pedido, titular, chave_painel in banco.execute(CONCILIA):
    if pedido is None:
        situacao = "🚩 denúncia sem pedido no painel"
    elif chave_vitima != chave_painel:
        situacao = "🚩 chave PIX diverge"
    else:
        situacao = "ok"
    problemas += situacao != "ok"
    linhas.append([den, data, pedido or "", titular or "", reais(centavos), situacao])

# Pedidos que ninguém denunciou ("vítimas silenciosas")
silenciosos = banco.execute("""
    SELECT COUNT(*) FROM pedidos AS p
     WHERE NOT EXISTS (SELECT 1 FROM denuncias AS d
                        WHERE d.nome = p.cliente AND d.data = p.data
                          AND d.valor_centavos = CAST(ROUND(p.valor * 100) AS INTEGER))""").fetchone()[0]

print(f"🔗 {len(linhas)} denúncias conferidas · {problemas} divergência(s) · "
      f"{silenciosos} pedido(s) sem denúncia (vítimas silenciosas)")

# Linha do tempo: quando cada conta começou a receber? (rotação de chaves)
print("\n🕰️  Entrada em uso de cada conta laranja:")
for titular, inicio, fim, n, centavos in banco.execute("""
        SELECT c.titular, MIN(p.data), MAX(p.data), COUNT(*), SUM(CAST(ROUND(p.valor*100) AS INTEGER))
          FROM pedidos p JOIN contas_recebimento c ON c.id = p.conta_id
         GROUP BY c.id ORDER BY MIN(p.data)"""):
    print(f"   {inicio} → {fim}  {titular:<28} {n:>2} pedidos  {reais(centavos)}")
print("   💡 Uma conta nova entra a cada poucos dias e todas seguem ativas até o fim: hipótese de")
print("      espalhar o dinheiro para não chamar atenção de um banco só. Hipótese, não conclusão.")

SAIDAS.mkdir(exist_ok=True)
with open(SAIDAS / "conciliacao.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["denuncia", "data", "pedido_painel", "titular_recebedor", "valor", "situacao"])
    w.writerows(linhas)
print("\n💾 saidas/conciliacao.csv gravado.")
banco.close()
