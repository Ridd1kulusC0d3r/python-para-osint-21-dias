"""
DNS sem dnspython: socket (A/AAAA) + DNS sobre HTTPS (MX, NS, TXT).

Carta 36 (rank A) — Jutsu do Registro Estruturado (parte 3)

O que você aprende:
  • a resolver IPs com socket.getaddrinfo (vem com o Python);
  • a pedir outros tipos de registro (MX, NS, TXT) a um resolvedor público via HTTPS;
  • a ler o SPF (registro TXT) para descobrir quem pode enviar e-mail pelo domínio.

Como rodar (dentro da pasta dia-15-dominios):
    python br/03_dns_doh.py
    OSINT_OFFLINE=1 python br/03_dns_doh.py
"""

import json
import os
import socket
import urllib.parse      # montar a URL com parâmetros (?name=...&type=...)
import urllib.request
from pathlib import Path

DOMINIO = "gov.br"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"

# Números oficiais de cada tipo de registro DNS (o resolvedor responde com eles).
TIPOS = {1: "A", 2: "NS", 5: "CNAME", 15: "MX", 16: "TXT", 28: "AAAA"}


def doh(nome, tipo):
    """Pergunta ao resolvedor público do Google via HTTPS. Devolve a lista 'Answer'."""
    url = "https://dns.google/resolve?" + urllib.parse.urlencode({"name": nome, "type": tipo})
    pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
    with urllib.request.urlopen(pedido, timeout=15) as resposta:
        return json.load(resposta).get("Answer", [])


# ── 1. IPs com socket (sem internet, isto falha, então tratamos o erro) ───
print(f"🌐 Domínio: {DOMINIO}\n")
if not OFFLINE:
    try:
        ips = {info[4][0] for info in socket.getaddrinfo(DOMINIO, None)}  # conjunto: sem repetidos
        for ip in sorted(ips):
            print(f"📍 IP: {ip}")
    except socket.gaierror as erro:
        print(f"⚠️ MODO OFFLINE: não foi possível resolver ({erro}).")

# ── 2. MX, NS e TXT via DNS sobre HTTPS ───────────────────────────────────
respostas = None
if not OFFLINE:
    try:
        respostas = {tipo: doh(DOMINIO, tipo) for tipo in ["MX", "NS", "TXT"]}
    except Exception as erro:
        print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
else:
    print("⚠️ MODO OFFLINE: usando a amostra local.")

if respostas is None:
    amostra = json.loads((PASTA_DIA / "dados" / "doh_gov_br.json").read_text(encoding="utf-8"))
    respostas = amostra["respostas"]

for tipo, lista in respostas.items():
    print(f"\n── {tipo} ──")
    for item in lista:
        print(f"  {TIPOS.get(item['type'], item['type']):<5} {item['data']}")

# ── 3. Bônus: o SPF entrega os provedores de e-mail usados ────────────────
for item in respostas.get("TXT", []):
    if "v=spf1" in item["data"]:
        includes = [p.split(":", 1)[1] for p in item["data"].strip('"').split() if p.startswith("include:")]
        print(f"\n✉️  SPF autoriza envio por: {', '.join(includes) or '(nenhum include)'}")
