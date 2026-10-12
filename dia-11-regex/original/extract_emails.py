# ──────────────────────────────────────────────────────────────────────────
# Título: Extrair e-mails de uma página com expressão regular
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_11/extract_emails.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install requests
# ──────────────────────────────────────────────────────────────────────────

# 💬 requests baixa a página; re (nativo) procura padrões de texto.
import requests

import re




# 💬 Página pública da CleanTalk sobre um e-mail em lista negra (alvo de exemplo do autor).
url = "https://cleantalk.org/blacklists/ivanov@gmail.com"

# 💬 .text devolve o HTML como string, pronto para a regex.
html = requests.get(url).text

# 💬 A regex lê-se assim: [a-zA-Z0-9-_.]+  → um ou mais caracteres de "nome";
# 💬 @ → a arroba; e de novo [a-zA-Z0-9-_.]+ → o "domínio".
# 💬 Atenção: dentro de [ ], o trecho "9-_" vira um INTERVALO (do '9' ao '_'), que inclui
# 💬 sem querer : ; < = > ? @ [ \ ] ^ e letras maiúsculas. Funciona, mas é mais largo do que parece.
# 💬 findall devolve uma LISTA com todos os trechos que casaram com o padrão.
result = re.findall("[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+", html)

# 💬 Imprime a lista (pode ter repetidos; no Dia 13 você aprende a tirá-los).
print(result)
