# ──────────────────────────────────────────────────────────────────────────
# Título: Data e hora atuais com datetime
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_19/date_time.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# ──────────────────────────────────────────────────────────────────────────
# 💬 datetime vem com o Python; não precisa instalar.
import datetime

# 💬 Hora local do computador, SEM fuso horário anexado ('ingênua').
# 💬 No Colab, o relógio está em UTC: 3 horas à frente de Brasília.
currentTime = datetime.datetime.now()

print(currentTime)

# 💬 year, month, day, hour... são atributos numéricos; str() converte para texto.
print("Current Year: "+str(currentTime.year))

print("Current Month: "+str(currentTime.month))

# 💬 strftime formata a data. %A e %B saem em INGLÊS (Monday, October)
# 💬 a menos que você mude o locale. Veja br/01_datas_br.py para pt-BR sem locale.
print(currentTime.strftime("%A %d %B %Y"))
