# ──────────────────────────────────────────────────────────────────────────
# Título: Salvar resultados de busca do DuckDuckGo num CSV (versão 2026)
# ATUALIZAÇÃO feita para este repositório, BASEADA no original de cipher387
# (Cyb_detective): https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_9/ddg_search_to_csv.py
# Licença: MIT © 2023 Cyb_detective (original). Troca ddg() (removida) por
# DDGS().text() do pacote "ddgs". O original continua em original/ddg_search_to_csv.py.
# Requer: pip install ddgs
# ──────────────────────────────────────────────────────────────────────────

from ddgs import DDGS
import csv

# Pequenas melhorias em relação ao original: newline="" e encoding="utf-8"
# (no Windows, sem isso, aparecem linhas vazias e acentos quebrados).
csv_file = open('search_results.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file, delimiter=';')

keywords = 'osint'
results = DDGS().text(keywords, region="us-en", safesearch="off", timelimit="y", max_results=10)

for x in range(len(results)):
    row = [results[x]["title"], results[x]["body"], results[x]["href"]]
    writer.writerow(row)

csv_file.close()
