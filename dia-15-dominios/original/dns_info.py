# ──────────────────────────────────────────────────────────────────────────
# Título: Descobrir o IP (registro A) de um domínio com dnspython
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_15/dns_info.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install dnspython
# ──────────────────────────────────────────────────────────────────────────

# 💬 "dns" é o pacote dnspython (não vem com o Python; precisa instalar).
import dns
# 💬 O módulo resolver faz as perguntas ao servidor DNS por nós.
import dns.resolver

# 💬 Pergunta: "qual é o registro A (endereço IPv4) de osintme.com?"
result = dns.resolver.resolve('osintme.com', 'A')
# 💬 Pode haver mais de um IP; percorremos todos.
for ipval in result:
    # 💬 to_text() transforma o objeto de resposta em texto legível.
    print('IP', ipval.to_text())
