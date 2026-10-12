# ──────────────────────────────────────────────────────────────────────────
# Título: Procurar um texto dentro de vários arquivos
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_14/check_files_contents.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────

import glob, os

os.chdir("test_dir")

# 💬 Percorre TODOS os arquivos da pasta (txt e csv).
for file in glob.glob("*"): 

    with open (file) as current_file:
        # 💬 read() traz o arquivo inteiro como uma string só.
        current_file_content=current_file.read()
        # 💬 "in" testa se o trecho "2" aparece em algum lugar do texto.
        if "2" in current_file_content:
             print(current_file_content)
