# ──────────────────────────────────────────────────────────────────────────
# Título: Percorrer as linhas de um arquivo numerando cada uma
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_4/read_lines_loop.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Não precisa instalar nada. Rode de dentro da pasta original/ (o results.txt está aqui).
# ──────────────────────────────────────────────────────────────────────────


# 💬 Contador que começa em 1 (para gente, a primeira linha é a 1, não a 0).
stringNumber = 1

# 💬 "with" abre o arquivo e FECHA sozinho no fim do bloco, mesmo se der erro.
with open("results.txt") as f:
    # 💬 Percorrer o arquivo com for lê uma linha por vez (economiza memória em arquivos grandes).
    for line in f:
        # 💬 str() transforma o número em texto para poder juntar com +.
        # 💬 A linha já termina com "\n" e o print pula outra: por isso sai uma linha em branco entre elas.
        print(str(stringNumber) + ". " + line)
        stringNumber += 1
