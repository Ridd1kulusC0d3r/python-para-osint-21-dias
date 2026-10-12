# ──────────────────────────────────────────────────────────────────────────
# Título: Ordenar uma lista (crescente e decrescente)
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_13/array_sort.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────

cities = ['New York', 'San Francisco', 'Houston', 'Los Angeles']

# 💬 sort() ordena a PRÓPRIA lista (não devolve nada). Para texto, a ordem é a dos códigos Unicode.
cities.sort()

print(cities)

# 💬 reverse=True inverte: de Z para A.
cities.sort(reverse=True)

print(cities)
