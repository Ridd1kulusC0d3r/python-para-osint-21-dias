# ──────────────────────────────────────────────────────────────────────────
# Título: Raspar o título (h1) de uma página do PyPI
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_10/scraping.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install requests beautifulsoup4
# ──────────────────────────────────────────────────────────────────────────

# 💬 requests baixa a página; BeautifulSoup (pacote beautifulsoup4) entende o HTML.
import requests
from bs4 import BeautifulSoup

# 💬 A página do PyPI de um pacote. Troque por outra página pública para testar.
url = "https://pypi.org/project/duckduckgo-search/"

# 💬 Faz o pedido HTTP GET. A resposta traz o HTML bruto em web_page.content.
web_page = requests.get(url)

# 💬 Cria a "sopa": o HTML vira uma árvore de elementos que dá para pesquisar.
# 💬 "html.parser" é o analisador que já vem com o Python (o lxml é mais rápido, mas precisa instalar).
soup = BeautifulSoup(web_page.content, "html.parser")

# 💬 find("h1") devolve o PRIMEIRO elemento <h1>; get_text() tira as tags e deixa só o texto.
# 💬 Se a página não tiver <h1>, find devolve None e get_text() dá AttributeError.
header = soup.find("h1").get_text()

# 💬 Mostra o título encontrado.
print(header)
