# ──────────────────────────────────────────────────────────────────────────
# Título: Buscar no DuckDuckGo a partir do Python
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_9/ddg_search.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer (na época): pip install duckduckgo_search
# ⚠️ Em 2026 este código NÃO roda mais: a função ddg() foi removida do pacote.
#    Use original/2026_ddg_search.py (versão atualizada com o pacote ddgs).
# ──────────────────────────────────────────────────────────────────────────

# 💬 ddg era uma função "atalho" do pacote duckduckgo_search (versões de 2022/2023).
from duckduckgo_search import ddg

# 💬 O termo de busca.
keywords = 'osint'
# 💬 region='us-en' = resultados dos EUA em inglês; safesearch='Off' = sem filtro;
# 💬 time='y' = só páginas do último ano (year).
results = ddg(keywords, region='us-en', safesearch='Off', time='y')
# 💬 results era uma lista de dicionários com title, href e body.
print(results)
