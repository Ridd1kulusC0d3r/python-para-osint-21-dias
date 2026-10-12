# ──────────────────────────────────────────────────────────────────────────
# Título: Ler as linhas de um arquivo como lista com readlines()
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_4/readlines.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Não precisa instalar nada. Rode de dentro da pasta original/ (o results.txt está aqui).
# ──────────────────────────────────────────────────────────────────────────

f = open("results.txt", "r")

# 💬 readlines() devolve uma LISTA: cada item é uma linha do arquivo (com o "\n" no fim).
stringList=f.readlines()

# 💬 [1] é a SEGUNDA linha (a contagem começa em 0). Se o arquivo tiver só uma
# 💬 linha, dá IndexError. Por isso o results.txt de exemplo já vem com várias.
print(stringList[1])
