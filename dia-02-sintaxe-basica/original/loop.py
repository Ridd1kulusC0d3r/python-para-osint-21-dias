# ──────────────────────────────────────────────────────────────────────────
# Título: Laços com for e range()
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_2/loop.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Não precisa instalar nada.
# ──────────────────────────────────────────────────────────────────────────

girls = ["Anna", "Maria", "Eva"]

# 💬 "Para cada girl na lista girls, faça...": o bloco recuado roda uma vez por item.
for girl in girls:
    print (girl +"; ")


# 💬 range(20) gera os números de 0 a 19 (vinte números, começando do zero).
# 💬 Este bloco usa 2 espaços de recuo; funciona, mas o padrão recomendado é 4.
for x in range(20):
  print(x)
