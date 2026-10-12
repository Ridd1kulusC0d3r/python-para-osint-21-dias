# ──────────────────────────────────────────────────────────────────────────
# Título: Primeiro pedido a uma API (busca de usuários no GitHub)
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_5/api_request.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install requests
# ──────────────────────────────────────────────────────────────────────────

# 💬 "requests" é o pacote mais famoso para fazer pedidos HTTP em Python.
# 💬 Ele não vem com o Python: precisa do pip install acima.
import requests

# 💬 GET = "me entregue esta página". A URL é a API de busca de usuários do GitHub;
# 💬 tudo depois do "?" é parâmetro: q=javascript significa "procure por javascript".
response = requests.get("https://api.github.com/search/users?q=javascript")

# 💬 A API responde em JSON; .json() transforma esse texto em dicionário Python.
# 💬 O print mostra tudo de uma vez (é muita coisa!). No Dia 6 aprendemos a escolher campos.
print(response.json())
