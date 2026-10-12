# ──────────────────────────────────────────────────────────────────────────
# Título: Testar uma lista de proxies até achar um que funcione
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_12/proxy_permulation.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install requests
# ──────────────────────────────────────────────────────────────────────────

import requests

# 💬 Lista de proxies "endereço:porta". Os nomes someproxyN.com são marcadores: não existem.
ip_addresses = [ "135.181.149.47:8080", "someproxy1.com:80", "someproxy2.com:80", "someproxy3.com:80", "someproxy4.com:80", "someproxy5.com:80", "someproxy6.com:80"]

url = 'https://cleantalk.org/blacklists/ivanov@gmail.com'

# 💬 Percorre a lista; para cada proxy monta o dicionário e tenta o pedido.
for proxy in ip_addresses:
    proxies = {'https': proxy}

   

    # 💬 try/except: se um proxy falhar, o laço segue para o próximo em vez de parar o script.
    try:
        response = requests.post(url, proxies=proxies)
        print(response.text)
    # 💬 "except:" sozinho pega QUALQUER erro (até Ctrl+C). Na camada BR usamos "except Exception".
    except:
         print("No")

