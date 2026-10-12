# ──────────────────────────────────────────────────────────────────────────
# Título: Acrescentar um item no fim da lista
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_13/array_append.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────

cities = ['New York', 'San Francisco', 'Houston', 'Los Angeles']

# 💬 append(item) põe o item no FIM da lista.
cities.append("Dallas")

# 💬 Curiosidade: sep só age entre VÁRIOS argumentos. Aqui há um só (a lista inteira),
# 💬 então o ";" não aparece. Para separar por ";" seria print(*cities, sep=";").
print(cities, sep=";")
