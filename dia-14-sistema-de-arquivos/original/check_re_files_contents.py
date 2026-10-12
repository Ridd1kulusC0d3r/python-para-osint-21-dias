# ──────────────────────────────────────────────────────────────────────────
# Título: Procurar e-mails (regex) em vários arquivos
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_14/check_re_files_contents.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────

import glob, os, re 

# 💬 re.compile prepara a regex uma vez só (a mesma do Dia 11) para reusar no laço.
regexp = re.compile('[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+')

os.chdir("test_dir")

for file in glob.glob("*"): 

    with open (file) as current_file:
        current_file_content=current_file.read()       
        # 💬 search procura o padrão em QUALQUER ponto do texto; devolve None se não achar.
        if regexp.search(current_file_content):
            # 💬 "Math" é um erro de digitação do autor para "Match" (correspondência). Mantido: é o original.
            print("Math in file: "+file)
            print(current_file_content)
