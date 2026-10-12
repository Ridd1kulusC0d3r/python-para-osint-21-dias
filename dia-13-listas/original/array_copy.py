# ──────────────────────────────────────────────────────────────────────────
# Título: Copiar uma lista
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_13/array_copy.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────

# 💬 Uma lista com 4 cidades dos EUA, entre colchetes e separadas por vírgula.
cities = ['New York', 'San Francisco', 'Houston', 'Los Angeles']

# 💬 copy() cria uma lista NOVA. Se fizesse copy_of_cities = cities, seriam dois nomes para a MESMA lista.
copy_of_cities = cities.copy()

# 💬 O * "espalha" os itens como argumentos separados; sep diz o que vai entre eles.
print(*copy_of_cities, sep = ", ")
