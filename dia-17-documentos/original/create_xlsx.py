# ──────────────────────────────────────────────────────────────────────────
# Título: Gerar uma planilha Excel (.xlsx) com XlsxWriter
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_17/create_xlsx.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install XlsxWriter
# ──────────────────────────────────────────────────────────────────────────
# 💬 XlsxWriter só ESCREVE arquivos .xlsx (para ler, use openpyxl).
import xlsxwriter


# 💬 O 'livro' (arquivo) e, abaixo, uma aba (planilha) vazia.
workbook = xlsxwriter.Workbook('employees.xlsx')
worksheet = workbook.add_worksheet()

# 💬 Uma tupla de listas: cada lista é uma linha [nome, idade]. A primeira é o cabeçalho.
employees = (
    ['Name', 'Age'],
    ['John Smith', 33],
    ['Eric Gold',   26],
    ['Simon Silver',  37],
    ['James Conor',    50],
)

# 💬 Contador de linha. No XlsxWriter a contagem começa em 0 (linha 0 = linha 1 do Excel).
row = 0

# 💬 Desempacota cada linha em duas variáveis e escreve na coluna 0 (A) e 1 (B).
for name, age in (employees):
    worksheet.write(row, 0, name)
    worksheet.write(row, 1, age)
    row += 1


# 💬 Depois do laço, 'row' aponta para a primeira linha livre.
worksheet.write(row, 0, 'Average age')
# 💬 Uma fórmula do Excel montada como texto. Atenção: row-1 faz o intervalo terminar
# 💬 uma linha antes do último funcionário (B1:B4) — confira no Excel e tente corrigir!
# 💬 Ah, e no Excel em português a função aparece como MÉDIA, mas o arquivo guarda 'AVERAGE'.
worksheet.write(row, 1, '=average(B1:B'+str(row-1)+')')

# 💬 Fechar é obrigatório: é aqui que o .xlsx é realmente gravado.
workbook.close()
