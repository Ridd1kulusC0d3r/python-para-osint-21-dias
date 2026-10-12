# ──────────────────────────────────────────────────────────────────────────
# Título: Buscar PDFs no DuckDuckGo e baixar os arquivos (versão 2026)
# ATUALIZAÇÃO feita para este repositório, BASEADA no original de cipher387
# (Cyb_detective): https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_9/ddg_search_download_pdf.py
# Licença: MIT © 2023 Cyb_detective (original). A opção download=True deixou de
# existir na API Python; aqui fazemos a busca com DDGS().text() e baixamos cada
# PDF com urllib (biblioteca padrão). O original continua intacto ao lado.
# Requer: pip install ddgs
# ──────────────────────────────────────────────────────────────────────────

import urllib.request
from pathlib import Path

from ddgs import DDGS

keywords = 'open source intelligence filetype:pdf'
max_results = 5                      # quantos arquivos, no máximo, vamos baixar

results = DDGS().text(keywords, region="us-en", safesearch="off", timelimit="y", max_results=max_results)

pasta = Path("pdfs_baixados")
pasta.mkdir(exist_ok=True)

for numero, resultado in enumerate(results, start=1):
    link = resultado["href"]
    if not link.lower().split("?")[0].endswith(".pdf"):
        continue                     # o buscador às vezes devolve páginas, não PDFs
    destino = pasta / f"{numero:02d}_{Path(link.split('?')[0]).name}"
    try:
        pedido = urllib.request.Request(link, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
        with urllib.request.urlopen(pedido, timeout=30) as resposta:
            destino.write_bytes(resposta.read())
        print("baixado:", destino)
    except Exception as erro:        # um link quebrado não deve parar os outros
        print("falhou:", link, erro)
