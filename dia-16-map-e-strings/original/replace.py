# ──────────────────────────────────────────────────────────────────────────
# Título: Trocar caracteres em várias palavras com replace()
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_16/replace.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────
# 💬 str.replace(velho, novo) troca TODAS as ocorrências de '_' por '-'.
def replaceDash(x):
  return x.replace("_","-")

# 💬 Palavras no estilo snake_case (com sublinhado).
words = ["six_pack","king_size","editor_in_chief"]

# 💬 Em OSINT isso vira gerador de variantes de username:
# 💬 kau_ofertas → kau-ofertas. Veja br/03_variantes_username.py.
result = map(replaceDash,words)

# 💬 Saída: ['six-pack', 'king-size', 'editor-in-chief']
print(list(result))
