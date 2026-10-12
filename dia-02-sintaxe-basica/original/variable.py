# ──────────────────────────────────────────────────────────────────────────
# Título: Variáveis e a função input()
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_2/variable.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Não precisa instalar nada. Este script usa input(): rode-o no terminal e responda.
# ──────────────────────────────────────────────────────────────────────────

# 💬 Uma variável é um nome que guarda um valor. Aqui, o texto "John".
first_name = "John"
# 💬 input() mostra a pergunta e ESPERA você digitar algo e apertar Enter.
# 💬 O que você digitar vira o valor de last_name. O \n pula uma linha depois da pergunta.
last_name = input('What is your last name?\n')
# 💬 O sinal + junta (concatena) textos. Por isso o " " no meio: sem ele, as palavras grudam.
print("You are" + " " + first_name+ " " + last_name)
 
