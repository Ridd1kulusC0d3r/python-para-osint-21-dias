# ──────────────────────────────────────────────────────────────────────────
# Título: Ler um campo de um JSON (total de resultados e o primeiro perfil)
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_6/read_one_field.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install requests
# ──────────────────────────────────────────────────────────────────────────

# 💬 json vem com o Python; requests precisa de pip install.
# 💬 (Curiosidade: aqui o json nem chega a ser usado, porque o requests já converte.)
import json
import requests

# 💬 O mesmo pedido do Dia 5: usuários do GitHub que combinam com "javascript".
response = requests.get("https://api.github.com/search/users?q=javascript")

# 💬 .json() transforma o texto da resposta num dicionário Python.
json_data=response.json()

# 💬 Colchetes com o nome do campo: pega o valor de "total_count" (quantos usuários existem).
print (json_data['total_count'])

# 💬 Caminho em três passos: a lista "items" → o item de posição 0 (o primeiro) → o campo "html_url".
print (json_data['items'][0]['html_url'])
