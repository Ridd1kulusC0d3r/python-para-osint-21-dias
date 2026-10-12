# ──────────────────────────────────────────────────────────────────────────
# Título: Gerar um PDF com fpdf2 (versão atualizada em 2026)
# ATUALIZAÇÃO 2026 feita para este repositório, BASEADA no original de cipher387
# (Day_17/create_pdf.py, MIT © 2023 Cyb_detective). O original continua intacto em
# create_pdf.py. Aqui só trocamos o que o fpdf2 marcou como obsoleto:
#   • txt=  → text=          (renomeado na versão 2.7.6)
#   • ln=2  → new_x / new_y  (ln está obsoleto desde a versão 2.5.2)
# Requer: pip install fpdf2   (rode dentro de original/, onde está o histogram.png)
# ──────────────────────────────────────────────────────────────────────────

# 💬 O fpdf2 mantém o mesmo nome de importação do pacote antigo.
from fpdf import FPDF
# 💬 XPos e YPos dizem para onde o "cursor" vai depois de escrever uma célula.
from fpdf.enums import XPos, YPos

pdfFile = FPDF()

pdfFile.add_page()

# 💬 "Helvetica" é o nome oficial da fonte embutida ("Arial" é só um apelido).
pdfFile.set_font("Helvetica", size=12)

# 💬 ln=2 do original significava "vá para a linha de baixo, mantendo a margem esquerda".
# 💬 No fpdf2 isso se escreve: new_x=XPos.LEFT, new_y=YPos.NEXT.
pdfFile.cell(20, 10, text="Report text", new_x=XPos.LEFT, new_y=YPos.NEXT, align="C")

pdfFile.image("histogram.png", 10, 40, 30)

pdfFile.output("report.pdf")
