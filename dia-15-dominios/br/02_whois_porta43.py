"""
WHOIS "na unha": conversando direto com o servidor na porta 43 (só stdlib).

Carta 36 (rank A) — Jutsu do Registro Estruturado (parte 2)

O que você aprende:
  • que o WHOIS é só uma conversa de texto numa porta TCP (a 43);
  • como perguntar à IANA qual servidor WHOIS cuida de cada terminação;
  • como transformar as linhas "campo: valor" em dicionário.

Por que manter WHOIS se existe RDAP? Porque muitos registros ainda respondem melhor
(ou só) por WHOIS, e porque o formato do registro.br traz campos úteis como
"owner", "owner-c" e "created". Analista bom sabe usar os dois.

Como rodar (dentro da pasta dia-15-dominios):
    python br/02_whois_porta43.py
    OSINT_OFFLINE=1 python br/02_whois_porta43.py
"""

import os                # ler OSINT_OFFLINE
import socket            # abrir uma conexão TCP crua (é tudo o que o WHOIS precisa)
from pathlib import Path

DOMINIO = "registro.br"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"


def whois(servidor, pergunta):
    """Abre a porta 43, envia a pergunta e devolve tudo o que o servidor responder."""
    with socket.create_connection((servidor, 43), timeout=15) as conexao:
        conexao.sendall((pergunta + "\r\n").encode())   # o protocolo pede \r\n no fim
        pedacos = []
        while True:
            pedaco = conexao.recv(4096)   # lemos de 4 em 4 KB...
            if not pedaco:                # ...até o servidor fechar a conexão
                break
            pedacos.append(pedaco)
    # Servidores antigos às vezes mandam latin-1; "replace" evita que o script quebre.
    return b"".join(pedacos).decode("utf-8", errors="replace")


def descobrir_servidor(dominio):
    """Pergunta à IANA (whois.iana.org) qual servidor WHOIS responde pela terminação."""
    tld = dominio.rsplit(".", 1)[-1]
    resposta = whois("whois.iana.org", tld)
    for linha in resposta.splitlines():
        if linha.lower().startswith("whois:"):          # ex.: "whois:  whois.registro.br"
            return linha.split(":", 1)[1].strip()
    return None


def em_dicionario(texto):
    """Converte linhas 'campo: valor' em {campo: [valores]} (campos podem repetir)."""
    campos = {}
    for linha in texto.splitlines():
        if ":" in linha and not linha.startswith("%"):  # "%" = comentário no registro.br
            chave, valor = linha.split(":", 1)
            campos.setdefault(chave.strip(), []).append(valor.strip())
    return campos


# ── Execução ──────────────────────────────────────────────────────────────
texto = None
if not OFFLINE:
    try:
        servidor = descobrir_servidor(DOMINIO)
        print(f"🔎 Servidor WHOIS indicado pela IANA: {servidor}")
        texto = whois(servidor, DOMINIO)
    except Exception as erro:
        print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
else:
    print("⚠️ MODO OFFLINE: usando a amostra local.")

if texto is None:
    texto = (PASTA_DIA / "dados" / "whois_registro_br.txt").read_text(encoding="utf-8")

campos = em_dicionario(texto)

# Mostramos só o que interessa numa investigação (o resto está em `texto`).
for chave in ["domain", "owner", "owner-c", "nserver", "created", "changed", "expires", "status"]:
    for valor in campos.get(chave, []):
        print(f"{chave:>8}: {valor}")
