# ──────────────────────────────────────────────────────────────────────────
# Título: Criar um arquivo CSV com cabeçalho e uma linha de dados
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_7/write_csv.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: nada (csv vem com o Python). Rode de dentro de original/: cria test.csv ali.
# ──────────────────────────────────────────────────────────────────────────

# 💬 O módulo csv vem com o Python.
import csv

# 💬 Abre (e cria) test.csv para escrita ("w" apaga o conteúdo anterior!).
# 💬 Dica 2026: no Windows, acrescente newline="" e encoding="utf-8" na sua versão,
# 💬 senão aparecem linhas em branco extras e acentos quebrados.
csv_file = open('test.csv', 'w')

# 💬 O "escritor" de CSV. delimiter=';' usa ponto e vírgula, como o Excel em português gosta.
writer = csv.writer(csv_file, delimiter =';')

# 💬 Uma lista = uma linha. Primeiro os nomes das colunas...
header = ['Last name', 'First name', 'Age', 'Country']

# 💬 ...depois os dados (exemplo do autor).
data = ['Smith', 'John', '35', 'USA']

writer.writerow(header)

writer.writerow(data)

# 💬 Fechar o arquivo garante que tudo foi gravado no disco.
csv_file.close()
