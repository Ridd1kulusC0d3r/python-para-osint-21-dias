# ──────────────────────────────────────────────────────────────────────────
# Título: Quebrar um texto em pedaços com split()
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_16/split_string.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────
# 💬 Uma linha com campos separados por ';' (como um CSV).
# 💬 Repare no ';' do final: ele gera um último pedaço VAZIO.
string = "first name;last name;email;address;"

# 💬 split(';') corta o texto em cada ';' e devolve uma lista.
fields = string.split(";")

# 💬 Percorre a lista e imprime um campo por linha (a última linha sai em branco).
for field in fields:
    print (field)
