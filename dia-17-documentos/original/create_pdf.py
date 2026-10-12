# ──────────────────────────────────────────────────────────────────────────
# Título: Gerar um PDF com FPDF
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_17/create_pdf.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install fpdf2  (o pacote antigo "fpdf" parou em 2017; o fpdf2 importa igual)
# ──────────────────────────────────────────────────────────────────────────
# 💬 Tanto o fpdf antigo quanto o fpdf2 usam 'from fpdf import FPDF'.
from fpdf import FPDF


# 💬 Cria o PDF (A4, retrato, medidas em milímetros por padrão).
pdfFile = FPDF()

# 💬 Todo PDF precisa de pelo menos uma página antes de escrever.
pdfFile.add_page()
 
# 💬 'Arial' é apelido da fonte embutida Helvetica. As fontes embutidas
# 💬 NÃO têm acentos fora do Latin-1 — para português completo, use add_font com um .ttf.
pdfFile.set_font("Arial", size = 12)

# 💬 Uma 'célula' de 20 x 10 mm com o texto centralizado. No fpdf2, txt= e ln= são OBSOLETOS:
# 💬 ainda funcionam, mas mostram aviso. Veja a versão atual em 2026_create_pdf.py.
pdfFile.cell(20, 10, txt = "Report text", ln = 2, align = 'C')

# 💬 Imagem em x=10 mm, y=40 mm, com 30 mm de largura.
pdfFile.image('histogram.png', 10, 40, 30)

# 💬 Grava o arquivo no disco.
pdfFile.output("report.pdf") 
