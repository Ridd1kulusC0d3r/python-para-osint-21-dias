# ──────────────────────────────────────────────────────────────────────────
# Título: Gerar um documento Word (.docx) com python-docx
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_17/create_docx.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install python-docx  (rode dentro de original/, onde está o histogram.png)
# ──────────────────────────────────────────────────────────────────────────
# 💬 O pacote se instala como 'python-docx', mas importa como 'docx'.
from docx import Document
# 💬 Inches converte polegadas para a unidade interna do Word.
from docx.shared import Inches

# 💬 Cria um documento em branco, na memória (ainda não existe arquivo).
document = Document()

# 💬 Nível 0 = título principal do documento.
document.add_heading('Report', 0)

# 💬 Nível 1 = título de seção (o 'Título 1' do Word).
document.add_heading('Report', level=1)


# 💬 Um parágrafo de texto comum.
document.add_paragraph(
    'Some text in report'
)

# 💬 Quebra de página: o que vier depois começa na página 2.
document.add_page_break()

# 💬 Insere a imagem com 1,25 polegada de largura (≈3,2 cm).
document.add_picture('histogram.png', width=Inches(1.25))

# 💬 Só agora o arquivo é gravado no disco.
document.save('report.docx')
