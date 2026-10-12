# ──────────────────────────────────────────────────────────────────────────
# Título: Ler o mesmo campo de todos os itens de uma lista JSON
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_6/read_list_of_fields.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install requests
# ──────────────────────────────────────────────────────────────────────────

import json
import requests

response = requests.get("https://api.github.com/search/users?q=javascript")

json_data=response.json()

# 💬 len() conta quantos itens vieram na lista (a API manda 30 por página).
# 💬 Atenção: o "-1" faz o laço pular o ÚLTIMO item. range(n) já vai de 0 até n-1,
# 💬 então bastaria len(json_data['items']). É um bom exemplo de erro "por um" (off-by-one).
usersCount = len(json_data['items'])-1

# 💬 x vale 0, 1, 2... e usamos x como posição na lista para imprimir cada perfil.
for x in range(usersCount):
    print (json_data['items'][x]['html_url'])
