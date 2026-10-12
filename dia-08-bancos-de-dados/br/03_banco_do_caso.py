"""
Criar o banco do caso (saidas/caso.db) a partir da planilha e consultar com segurança.

Carta 29 (rank B) — Jutsu do Arquivo Morto (parte 3)

O que você aprende:
  • a criar um arquivo SQLite de verdade e importar um CSV com executemany;
  • a guardar dinheiro em CENTAVOS (INTEGER) para nunca errar soma;
  • consultas parametrizadas com "?" e por que isso evita SQL injection;
  • consultas por cidade e por mês com GROUP BY e strftime.

Como rodar (dentro da pasta dia-08-bancos-de-dados):
    python br/03_banco_do_caso.py
"""

import csv
import sqlite3
from decimal import Decimal
from pathlib import Path

CIDADE = "Belo Horizonte"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"


def reais(centavos):
    valor = Decimal(centavos) / 100
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ── 1. Criar o arquivo do banco (do zero, a cada execução) ────────────────
SAIDAS.mkdir(exist_ok=True)
caminho_db = SAIDAS / "caso.db"
caminho_db.unlink(missing_ok=True)            # apaga a versão anterior, se houver
banco = sqlite3.connect(caminho_db)

banco.execute("""
    CREATE TABLE denuncias (
        id             TEXT PRIMARY KEY,
        data           TEXT NOT NULL,      -- AAAA-MM-DD (texto ISO ordena certinho)
        cidade         TEXT,
        uf             TEXT,
        valor_centavos INTEGER NOT NULL,   -- 149.90 vira 14990
        produto        TEXT,
        chave_pix      TEXT
    )
""")

# ── 2. Importar o CSV ─────────────────────────────────────────────────────
# Minimização (LGPD): NÃO levamos nome, CPF nem telefone para este banco de análise.
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8", newline="") as arquivo:
    linhas = [
        (d["id"], d["data"], d["cidade"], d["uf"], int(Decimal(d["valor"]) * 100), d["produto"],
         d["chave_pix_destino"])
        for d in csv.DictReader(arquivo, delimiter=";")
    ]
# executemany roda o mesmo INSERT para cada tupla. Os "?" são preenchidos pelo SQLite.
banco.executemany("INSERT INTO denuncias VALUES (?, ?, ?, ?, ?, ?, ?)", linhas)
banco.commit()                                 # grava de verdade no arquivo
print(f"🗄️  {len(linhas)} denúncias importadas para {caminho_db.relative_to(PASTA_DIA)}\n")

# ── 3. Consulta por mês ───────────────────────────────────────────────────
print("📅 Por mês:")
for mes, qtd, centavos in banco.execute("""
        SELECT strftime('%Y-%m', data) AS mes, COUNT(*), SUM(valor_centavos)
          FROM denuncias GROUP BY mes ORDER BY mes"""):
    print(f"   {mes}  {qtd:>2} denúncias  {reais(centavos):>13}")

# ── 4. Consulta por cidade (como foi digitada; a padronização foi o Dia 7) ─
print("\n🏙️  Top 5 cidades (grafia original):")
for cidade, qtd in banco.execute(
        "SELECT cidade, COUNT(*) AS n FROM denuncias GROUP BY cidade ORDER BY n DESC, cidade LIMIT 5"):
    print(f"   {cidade:<22} {qtd}")

# ── 5. Consulta PARAMETRIZADA ─────────────────────────────────────────────
# O valor do usuário vai SEPARADO do comando, no lugar do "?". O SQLite trata como dado, nunca
# como código. lower() dos dois lados faz "belo horizonte" e "Belo Horizonte" baterem.
consulta_segura = "SELECT COUNT(*), SUM(valor_centavos) FROM denuncias WHERE lower(cidade) = lower(?)"
qtd, centavos = banco.execute(consulta_segura, (CIDADE,)).fetchone()
print(f"\n🔎 Denúncias em {CIDADE!r}: {qtd} · {reais(centavos or 0)}")
print("   (\"Belo Horizone\", com erro de digitação, NÃO entra: por isso padronizamos no Dia 7.)")

# ── 6. Por que NUNCA montar SQL juntando texto ────────────────────────────
ataque = "x' OR '1'='1"                         # o que um usuário malicioso digitaria
perigosa = f"SELECT COUNT(*) FROM denuncias WHERE cidade = '{ataque}'"
print("\n☠️  SQL injection, demonstração:")
print(f"   comando montado com f-string: {perigosa}")
print(f"   resultado: {banco.execute(perigosa).fetchone()[0]} linhas  ← devolveu TUDO!")
segura = banco.execute("SELECT COUNT(*) FROM denuncias WHERE cidade = ?", (ataque,)).fetchone()[0]
print(f"   mesma entrada com '?': {segura} linhas  ← tratado como texto comum, inofensivo")
banco.close()
