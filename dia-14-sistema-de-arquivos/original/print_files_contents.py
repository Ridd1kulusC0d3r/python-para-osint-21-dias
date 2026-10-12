# ──────────────────────────────────────────────────────────────────────────
# Título: Mostrar o conteúdo dos arquivos .txt
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_14/print_files_contents.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────

import glob, os

os.chdir("test_dir")

# 💬 Para cada .txt encontrado...
for file in glob.glob("*.txt"): 

    # 💬 ...abre o arquivo. Sem encoding=, o Python usa o padrão do sistema (no Windows pode ser cp1252).
    with open (file) as current_file:
        # 💬 readlines() devolve uma LISTA de linhas, cada uma terminando em \n.
        print(current_file.readlines())
