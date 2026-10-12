# ──────────────────────────────────────────────────────────────────────────
# Título: Inserir um item numa posição
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_13/array_insert.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────

cities = ['New York', 'San Francisco', 'Houston', 'Los Angeles']

# 💬 insert(posição, item): a contagem começa em 0, então 3 é a QUARTA posição.
# 💬 "Los Angeles" é empurrada uma casa para a direita.
cities.insert(3,"Dallas")

print(cities)
