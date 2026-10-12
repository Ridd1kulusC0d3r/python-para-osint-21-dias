# ──────────────────────────────────────────────────────────────────────────
# Título: Rodar o blackbird de dentro do Python com subprocess
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_3/launch.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: o blackbird clonado (git clone https://github.com/p1ngul1n0/blackbird),
#         pip install -r requirements.txt, e este arquivo DENTRO da pasta blackbird/.
# ──────────────────────────────────────────────────────────────────────────

# 💬 subprocess vem com o Python: serve para rodar outros programas como se você
# 💬 tivesse digitado o comando no terminal.
import subprocess
# 💬 Roda "python blackbird.py -u ivanov": procura o nome de usuário "ivanov" em
# 💬 centenas de sites. shell=True entrega o texto inteiro para o terminal interpretar.
# 💬 Em 2026 a opção -u (ou --username) continua igual no blackbird.
# 💬 No macOS/Linux, se "python" não existir, troque por "python3" no texto do comando.
subprocess.call("python blackbird.py -u ivanov", shell=True)
