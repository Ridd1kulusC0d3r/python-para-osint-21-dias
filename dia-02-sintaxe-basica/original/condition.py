# ──────────────────────────────────────────────────────────────────────────
# Título: Condições com if e elif
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_2/condition.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Não precisa instalar nada. Este script usa input(): rode-o no terminal e responda.
# ──────────────────────────────────────────────────────────────────────────

# 💬 input() SEMPRE devolve texto, mesmo que você digite um número.
age = input('How old are you?\n')


# 💬 int(age) converte o texto em número inteiro para poder comparar com 27.
# 💬 Repare nos 4 espaços antes do print: é assim que o Python sabe o que está "dentro" do if.
if int(age) > 27:
    print("You are so old")
# 💬 elif = "senão, se...". Só é testado se a condição de cima for falsa.
# 💬 Pergunta para você: o que acontece se a idade for exatamente 27?
elif int(age) < 27:
    print("You are so young")
