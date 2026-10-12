# ──────────────────────────────────────────────────────────────────────────
# Título: Converter um dump .sql em arquivos CSV (uma tabela por arquivo)
# NÃO HÁ CÓDIGO DO AUTOR NESTE DIA. Esta é uma RECONSTRUÇÃO da prática proposta
# por cipher387 (Cyb_detective) no Dia 8 de "Python for OSINT. 21-day course":
# "converta o dump para CSV e abra numa planilha". Escrita para este repositório,
# só com a biblioteca padrão, usando o dump FICTÍCIO de caso/dados/.
# Licença: MIT (a mesma do repositório).
# ──────────────────────────────────────────────────────────────────────────

import csv
import sqlite3            # banco de dados SQLite: vem com o Python
from pathlib import Path

# Pasta do dia (funciona como script e no Colab)
PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
DUMP = PASTA_DIA.parent / "caso" / "dados" / "painel_dump.sql"
SAIDAS = PASTA_DIA / "saidas"

# 1. Um banco "de mentirinha" que vive só na memória RAM (some ao fim do script).
#    Assim nada do dump é gravado em disco sem querermos.
banco = sqlite3.connect(":memory:")

# 2. executescript roda todos os comandos do arquivo de uma vez (CREATE TABLE, INSERT…).
#    Isto funciona porque o dump fictício foi escrito em SQL compatível com SQLite.
#    Dumps de MySQL/PostgreSQL reais costumam ter comandos que o SQLite não entende.
banco.executescript(DUMP.read_text(encoding="utf-8"))

# 3. Descobrir quais tabelas existem (o SQLite guarda isso na tabela especial sqlite_master).
tabelas = [linha[0] for linha in banco.execute(
    "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name")]

# 4. Exportar cada tabela para um CSV com cabeçalho.
SAIDAS.mkdir(exist_ok=True)
for tabela in tabelas:
    # Nome de tabela não pode ir como parâmetro "?"; aqui ele vem do próprio sqlite_master.
    cursor = banco.execute(f'SELECT * FROM "{tabela}"')
    colunas = [descricao[0] for descricao in cursor.description]   # nomes das colunas
    destino = SAIDAS / f"{tabela}.csv"
    with open(destino, "w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(colunas)
        escritor.writerows(cursor)                                  # todas as linhas
    total = banco.execute(f'SELECT COUNT(*) FROM "{tabela}"').fetchone()[0]
    print(f"💾 {tabela:<20} {total:>3} linhas → {destino.relative_to(PASTA_DIA)}")

banco.close()
print("\n✅ Pronto: abra os CSVs no Excel, LibreOffice ou Google Planilhas.")
