# ──────────────────────────────────────────────────────────────────────────
# Título: Fazer um pedido HTTP passando por um proxy
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_12/simple_proxy.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install requests
# ──────────────────────────────────────────────────────────────────────────

# 💬 requests aceita um dicionário "proxies" que diz por onde o tráfego deve passar.
import requests


# 💬 Chave 'https' = proxy usado para endereços https://. O IP do autor provavelmente já não funciona:
# 💬 troque por um proxy que VOCÊ controla ou contratou (leia a seção de ética do README).
proxies = {
  'https': '135.181.149.47:8080',
}


# 💬 Mesmo alvo do Dia 11.
url = 'https://cleantalk.org/blacklists/ivanov@gmail.com'


# 💬 O autor usa POST; para só ler a página, GET seria o mais comum.
# 💬 Se o proxy estiver fora do ar, aqui sai um erro (ProxyError/ConnectTimeout).
response = requests.post(url, proxies=proxies)


# 💬 O site vê o IP do proxy, não o seu.
print(response.text)
