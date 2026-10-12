# ──────────────────────────────────────────────────────────────────────────
# Título: Só a primeira letra maiúscula com capitalize()
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_16/capfirstword.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────
# 💬 str.capitalize() deixa maiúscula só a PRIMEIRA letra do texto todo
# 💬 (e põe o resto em minúsculas).
def capitalizeFirstWord(x):
  return x.capitalize()

cities = ["new york","los angeles","chicago"]

# 💬 Mesma lista, outra função: compare com capallwords.py.
result = map(capitalizeFirstWord,cities)

# 💬 Saída: ['New york', 'Los angeles', 'Chicago']
print(list(result))
