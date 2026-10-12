# ──────────────────────────────────────────────────────────────────────────
# Título: Buscar PDFs no DuckDuckGo e baixar os arquivos encontrados
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_9/ddg_search_download_pdf.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer (na época): pip install duckduckgo_search
# ⚠️ Em 2026 este código NÃO roda mais (ddg() e a opção download=True foram removidas).
#    Veja original/2026_ddg_search_download_pdf.py.
# ──────────────────────────────────────────────────────────────────────────

from duckduckgo_search import ddg

# 💬 filetype:pdf é um operador de busca: só traz arquivos PDF.
keywords = 'open source intelligence filetype:pdf'
# 💬 download=True mandava o pacote baixar cada arquivo encontrado para uma pasta local.
# 💬 O autor lembra que max_results controla quantos arquivos são baixados.
results = ddg(keywords, region='us-en', safesearch='Off', time='y', download=True)
