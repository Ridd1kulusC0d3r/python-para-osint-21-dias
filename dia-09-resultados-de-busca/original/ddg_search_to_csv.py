# ──────────────────────────────────────────────────────────────────────────
# Título: Salvar resultados de busca do DuckDuckGo num CSV
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_9/ddg_search_to_csv.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer (na época): pip install duckduckgo_search
# ⚠️ Em 2026 este código NÃO roda mais (ddg() foi removida).
#    Use original/2026_ddg_search_to_csv.py.
# ──────────────────────────────────────────────────────────────────────────

from duckduckgo_search import ddg
import csv

# 💬 Mesmo padrão do Dia 7: arquivo aberto para escrita e separador ";".
csv_file = open('search_results.csv', 'w')
writer = csv.writer(csv_file, delimiter =';')


keywords = 'osint'
results = ddg(keywords, region='us-en', safesearch='Off', time='y')

# 💬 Uma linha do CSV por resultado: título, resumo (body) e link (href).
for x in range(len(results)):
    row = [results[x]["title"],results[x]["body"],results[x]["href"]]
    writer.writerow(row)

csv_file.close()
