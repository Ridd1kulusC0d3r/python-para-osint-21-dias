# ──────────────────────────────────────────────────────────────────────────
# Título: Buscar no DuckDuckGo a partir do Python (versão 2026)
# ATUALIZAÇÃO feita para este repositório, BASEADA no original de cipher387
# (Cyb_detective): https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_9/ddg_search.py
# Licença: MIT © 2023 Cyb_detective (original). Por que existe: a função ddg()
# do pacote duckduckgo_search foi removida; o pacote hoje se chama "ddgs" e usa
# a classe DDGS. O original continua intacto em original/ddg_search.py.
# Requer: pip install ddgs
# ──────────────────────────────────────────────────────────────────────────

from ddgs import DDGS

keywords = 'osint'

# Antes: ddg(keywords, region='us-en', safesearch='Off', time='y')
# Agora: o parâmetro "time" virou "timelimit", safesearch é minúsculo ("off")
# e max_results diz quantos resultados queremos.
results = DDGS().text(keywords, region="us-en", safesearch="off", timelimit="y", max_results=10)

# Continua sendo uma lista de dicionários com as chaves title, href e body.
print(results)
