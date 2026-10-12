# ──────────────────────────────────────────────────────────────────────────
# Título: Baixar cópias antigas de um site da Wayback Machine
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_19/download_mementos.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install wayback  (demora: baixa várias páginas da Wayback Machine)
# ──────────────────────────────────────────────────────────────────────────
# 💬 Pacote 'wayback' (mantido pela EDGI) que conversa com a API do Internet Archive.
import wayback
from datetime import datetime

# 💬 O cliente cuida das requisições e dos limites de velocidade.
client = wayback.WaybackClient()

# 💬 search() consulta o índice CDX: cada 'record' é UMA captura (data, URL, status...).
# 💬 to_date limita às capturas feitas antes de 01/01/1999.
for record in client.search('http://nasa.gov', to_date=datetime(1999, 1, 1)):

    # 💬 'Memento' é a cópia arquivada em si: aqui o HTML é baixado de verdade.
    memento = client.get_memento(record)

    # 💬 Troca '/' por '-' porque '/' não pode aparecer em nome de arquivo.
    fileName=memento.memento_url.replace("/","-")+".html"

    # 💬 Modo 'a' (acrescentar). Sem encoding='utf-8', no Windows pode dar erro de acento.
    memento_file = open(fileName, "a")

    memento_file.write(memento.text)

    memento_file.close()

    print (fileName)
