"""
Explorar um dump SQL desconhecido: que tabelas, que colunas, quantas linhas?

Carta 29 (rank B) — Jutsu do Arquivo Morto

O que você aprende:
  • a carregar um .sql no SQLite (biblioteca padrão) sem instalar servidor de banco;
  • a listar tabelas pela tabela especial sqlite_master;
  • a ver as colunas e os tipos com PRAGMA table_info;
  • a espiar as primeiras linhas com LIMIT antes de fazer qualquer conta.

Regra da Iara: "antes de perguntar ao banco, descubra o que o banco sabe".

Como rodar (dentro da pasta dia-08-bancos-de-dados):
    python br/01_explorar_dump.py
"""

import hashlib              # impressão digital do arquivo (cadeia de custódia, Dia 14)
import sqlite3
from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
DUMP = PASTA_DIA.parent / "caso" / "dados" / "painel_dump.sql"

# ── 0. Antes de abrir: registrar o hash do arquivo recebido ───────────────
# Se alguém questionar "esse dump foi alterado?", o SHA-256 responde.
conteudo = DUMP.read_bytes()
print(f"🧾 Arquivo: {DUMP.name} · {len(conteudo)} bytes")
print(f"🔐 SHA-256: {hashlib.sha256(conteudo).hexdigest()}\n")

# ── 1. Carregar em memória ────────────────────────────────────────────────
banco = sqlite3.connect(":memory:")
banco.executescript(conteudo.decode("utf-8"))

# ── 2. Que tabelas existem? ───────────────────────────────────────────────
# sqlite_master é o "índice" do banco: guarda nome e o comando que criou cada tabela.
tabelas = banco.execute(
    "SELECT name, sql FROM sqlite_master WHERE type = 'table' ORDER BY name").fetchall()
print(f"🗄️  {len(tabelas)} tabela(s) encontrada(s):")

for nome, comando in tabelas:
    total = banco.execute(f'SELECT COUNT(*) FROM "{nome}"').fetchone()[0]
    print(f"\n── {nome} ({total} linhas) ──")
    print(f"   criada com: {comando}")

    # ── 3. Colunas e tipos ────────────────────────────────────────────────
    # PRAGMA table_info devolve: (posição, nome, tipo, not null?, valor padrão, chave primária?)
    for posicao, coluna, tipo, _nao_nulo, _padrao, chave in banco.execute(f'PRAGMA table_info("{nome}")'):
        marca = " 🔑 chave primária" if chave else ""
        print(f"   {posicao}. {coluna:<12} {tipo:<8}{marca}")

    # ── 4. As 3 primeiras linhas (LIMIT) ──────────────────────────────────
    print("   primeiras linhas:")
    for linha in banco.execute(f'SELECT * FROM "{nome}" LIMIT 3'):
        print(f"     {linha}")

# ── 5. Uma pista estrutural ───────────────────────────────────────────────
# A coluna pedidos.conta_id guarda um número que bate com contas_recebimento.id.
# Isso é uma "chave estrangeira": é o fio que liga cada pedido à conta que recebeu o PIX.
print("\n🧵 Pista: pedidos.conta_id ↔ contas_recebimento.id. No próximo script usamos esse fio")
print("   para descobrir quem recebeu cada real.")
banco.close()
