# ──────────────────────────────────────────────────────────────────────────
# Título: Listar nomes de arquivos de uma pasta
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_14/print_files_names.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────

# 💬 glob acha arquivos por "curinga" (*.txt); os conversa com o sistema operacional.
import glob, os

# 💬 Entra na pasta test_dir. Por isso rode este script DE DENTRO de original/ (cd original).
os.chdir("test_dir")


print ("TXT files")
# 💬 "*.txt" = qualquer nome que termine em .txt.
for file in glob.glob("*.txt"): 
    print(file)

print ("ALL files")
# 💬 "*" = todos os arquivos (a ordem pode variar de sistema para sistema).
for file in glob.glob("*"): 
    print(file)
