# ──────────────────────────────────────────────────────────────────────────
# Título: Ler só a primeira coluna de um CSV
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_7/read_csv_one_column.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: rode antes original/write_csv.py para criar test.csv.
# ──────────────────────────────────────────────────────────────────────────

import csv

with open("test.csv", 'r') as csv_file:
  csv_reader = csv.reader(csv_file)
  for row in csv_reader: 
    # 💬 Como o leitor usou vírgula, row[0] é a linha inteira; o autor separa no ";" na mão.
    # 💬 Funciona, mas quebra se algum campo tiver ";" dentro de aspas. A forma robusta é
    # 💬 csv.reader(csv_file, delimiter=';') e depois row[0] (veja br/01_ler_denuncias.py).
    columns=row[0].split(";")
    print(columns[0])
