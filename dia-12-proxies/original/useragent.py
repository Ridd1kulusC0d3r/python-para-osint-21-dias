# ──────────────────────────────────────────────────────────────────────────
# Título: Enviar um User-Agent personalizado
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_12/useragent.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install requests
# ──────────────────────────────────────────────────────────────────────────

# 💬 O cabeçalho User-Agent diz ao site qual navegador/sistema está pedindo a página.
import requests

# 💬 Site que mostra o que o seu navegador revela. Hoje ele pode bloquear robôs (Cloudflare).
url = 'https://www.whatismybrowser.com/'

# 💬 Um UA de Chrome 45 no Windows 7 (de 2015). Um UA tão velho também chama atenção!
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
}

# 💬 Sem esse headers, o requests se apresenta como "python-requests/2.x", o que denuncia o robô.
response = requests.get(url, headers=headers)

print(response.text)
