# ──────────────────────────────────────────────────────────────────────────
# Título: Escrever (acrescentar) texto num arquivo
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_4/write_text.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Não precisa instalar nada. Rode de dentro da pasta original/ (o results.txt está aqui).
# ──────────────────────────────────────────────────────────────────────────

result = "Results text"

# 💬 Modo "a" (append): ACRESCENTA no fim do arquivo; se ele não existir, cria.
# 💬 Outros modos: "w" apaga tudo e escreve do zero; "x" só cria se ainda não existir; "r" só lê.
results_file = open("results.txt", "a")

# 💬 write() não pula linha sozinho. Rodando duas vezes, fica "Results textResults text".
results_file.write(result)

# 💬 close() garante que tudo foi gravado no disco.
results_file.close()
