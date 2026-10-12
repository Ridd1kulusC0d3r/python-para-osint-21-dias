# ──────────────────────────────────────────────────────────────────────────
# Título: Primeira letra maiúscula em todas as palavras com title()
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_16/capallwords.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────
# 💬 str.title() põe maiúscula no começo de CADA palavra.
def capitalizeAllWords(x):
  return x.title()

# 💬 Cidades dos EUA, todas em minúsculas.
cities = ["new york","los angeles","chicago"]

# 💬 Aplica a função em cada cidade.
result = map(capitalizeAllWords,cities)

# 💬 Saída: ['New York', 'Los Angeles', 'Chicago'].
# 💬 Em nomes brasileiros, title() erra: 'Maria Da Silva'. Veja br/01_nomes_br.py.
print(list(result))
