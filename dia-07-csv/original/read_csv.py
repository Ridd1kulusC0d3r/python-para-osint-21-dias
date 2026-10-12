# ──────────────────────────────────────────────────────────────────────────
# Título: Ler um arquivo CSV linha por linha
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_7/read_csv.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: rode antes original/write_csv.py (ou json_to_csv.py) para criar test.csv.
# ──────────────────────────────────────────────────────────────────────────

import csv

# 💬 "with" abre o arquivo e fecha sozinho no final do bloco. 'r' = só leitura.
with open("test.csv", 'r') as csv_file:
  # 💬 Sem delimiter, o leitor espera VÍRGULA. Como o arquivo usa ";", cada linha
  # 💬 vem como uma lista com um único texto: ['Smith;John;35;USA'].
  csv_reader = csv.reader(csv_file)
  for row in csv_reader:
    print(row)
