# ──────────────────────────────────────────────────────────────────────────
# Título: Converter a resposta JSON da API do GitHub em CSV
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_7/json_to_csv.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install requests
# ──────────────────────────────────────────────────────────────────────────

import json
import requests
import csv


# 💬 O mesmo pedido dos Dias 5 e 6.
response = requests.get("https://api.github.com/search/users?q=javascript")

json_data=response.json()


# 💬 Atenção: isto SOBRESCREVE o test.csv criado pelo write_csv.py.
csv_file = open('test.csv', 'w')

writer = csv.writer(csv_file, delimiter =';')

# 💬 O mesmo "- 1" do Dia 6: o último usuário da página fica de fora.
usersCount = len(json_data['items'])-1

# 💬 Para cada usuário, monta uma linha com 3 colunas: login, perfil e foto.
for x in range(usersCount):
    row = []
    row.append(json_data['items'][x]['login'])
    row.append(json_data['items'][x]['html_url'])
    row.append(json_data['items'][x]['avatar_url'])
    writer.writerow(row)
   

csv_file.close()





