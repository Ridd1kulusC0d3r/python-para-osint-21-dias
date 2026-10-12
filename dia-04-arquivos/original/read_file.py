# ──────────────────────────────────────────────────────────────────────────
# Título: Ler um arquivo inteiro com read()
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_4/read_file.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Não precisa instalar nada. Rode de dentro da pasta original/ (o results.txt está aqui).
# ──────────────────────────────────────────────────────────────────────────

# 💬 open(nome, "r") abre o arquivo para LEITURA ("r" de read).
# 💬 O caminho é relativo: o Python procura results.txt na pasta onde você está.
results_file = open("results.txt", "r")

# 💬 read() devolve o conteúdo INTEIRO como um único texto.
# 💬 O original não fecha o arquivo; o Python fecha sozinho quando o script termina.
print(results_file.read())
