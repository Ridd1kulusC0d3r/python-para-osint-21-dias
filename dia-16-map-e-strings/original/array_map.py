# ──────────────────────────────────────────────────────────────────────────
# Título: Aplicar uma função a cada item de uma lista com map()
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_16/array_map.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────
# 💬 Uma função simples: recebe um número e devolve o dobro.
def doubleNumber(x):
  return x * 2

# 💬 A lista que vai passar pela função, item por item.
numbers = [2,4,8]

# 💬 map(função, lista) aplica a função em CADA item. Repare: passamos
# 💬 o NOME da função, sem parênteses (não estamos chamando, estamos entregando).
result = map(doubleNumber,numbers)

# 💬 map() devolve um objeto 'preguiçoso'; list() força o cálculo e mostra tudo.
# 💬 Saída esperada: [4, 8, 16]
print(list(result))
