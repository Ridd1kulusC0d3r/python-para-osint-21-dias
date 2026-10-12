# ──────────────────────────────────────────────────────────────────────────
# Título: Listas: criar, acrescentar e acessar por índice
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_2/list.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Não precisa instalar nada.
# ──────────────────────────────────────────────────────────────────────────

# 💬 Uma lista guarda vários valores em ordem, entre colchetes e separados por vírgula.
girls = ["Anna", "Maria", "Eva"]
print(girls)

# 💬 append() acrescenta um item no FIM da lista.
girls.append("Brenda")
print(girls)

# 💬 A contagem começa em ZERO: [0] é "Anna", [1] é "Maria"... então [3] é "Brenda".
print (girls[3])
