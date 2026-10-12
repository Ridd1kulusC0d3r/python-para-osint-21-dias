# ──────────────────────────────────────────────────────────────────────────
# Título: Consulta WHOIS de um domínio com python-whois
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_15/whois_info.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install python-whois
# ──────────────────────────────────────────────────────────────────────────

# 💬 O pacote python-whois consulta o WHOIS e já entrega os campos separados.
import whois 

# 💬 Consulta o domínio sector035.nl (site de OSINT holandês, o alvo do autor).
whois_info = whois.whois('sector035.nl')

# 💬 Mostra tudo o que veio na resposta.
print (whois_info)

print("Creation date")

# 💬 A data de criação é um dos campos mais valiosos: domínio novo + promoção
# 💬 boa demais é um sinal clássico de golpe.
print(whois_info["creation_date"])
