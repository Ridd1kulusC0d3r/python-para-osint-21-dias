"""
Qual IP o site enxerga? E como mandar o pedido por um proxy (só stdlib).

Carta 33 (rank A) — Jutsu do Disfarce Digital

O que você aprende:
  • que todo site que você visita vê um endereço IP: o seu ou o de quem está no meio;
  • a perguntar "qual é o meu IP público?" para a API do ipify;
  • a usar urllib.request.ProxyHandler para passar por um proxy;
  • a ler o endereço do proxy de uma variável de ambiente (sem gravar senha no código).

Como usar um proxy (opcional): defina a variável PROXY_URL antes de rodar.
    Linux/macOS:  export PROXY_URL="http://usuario:senha@meu-proxy.exemplo:3128"
    Windows (PowerShell):  $env:PROXY_URL="http://meu-proxy.exemplo:3128"

Como rodar (dentro da pasta dia-12-proxies):
    python br/01_meu_ip.py
    OSINT_OFFLINE=1 python br/01_meu_ip.py
"""

import json
import os
import urllib.request
from pathlib import Path

URL_IP = "https://api.ipify.org?format=json"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"

# ── 1. Há um proxy configurado? ───────────────────────────────────────────
# os.environ.get devolve None se a variável não existir: o script funciona dos dois jeitos.
PROXY_URL = os.environ.get("PROXY_URL")


def esconder_senha(url):
    """'http://ana:segredo@proxy:3128' → 'http://ana:***@proxy:3128' (nunca imprima senha!)."""
    if url and "@" in url and ":" in url.split("@")[0].split("//")[-1]:
        inicio, resto = url.split("//", 1)
        credenciais, host = resto.split("@", 1)
        return f"{inicio}//{credenciais.split(':')[0]}:***@{host}"
    return url


def montar_abridor():
    """Cria o 'abridor' de URLs: com proxy, se PROXY_URL existir; senão, o padrão."""
    if PROXY_URL:
        # O mesmo proxy para http:// e https://. O urllib conversa com ele e ele com o site.
        manipulador = urllib.request.ProxyHandler({"http": PROXY_URL, "https": PROXY_URL})
        print(f"🧥 Usando proxy: {esconder_senha(PROXY_URL)}")
    else:
        # Sem argumento, o ProxyHandler lê HTTP_PROXY/HTTPS_PROXY do sistema (se houver).
        manipulador = urllib.request.ProxyHandler()
        do_sistema = {k: v for k, v in urllib.request.getproxies().items() if k in ("http", "https")}
        if do_sistema:
            print(f"ℹ️  PROXY_URL não definido, mas o sistema já tem proxy: {list(do_sistema)}")
        else:
            print("ℹ️  Sem proxy: o site vai ver o IP da sua conexão.")
    return urllib.request.build_opener(manipulador)


def buscar_json(url, amostra):
    """Baixa um JSON pelo abridor; se falhar (ou OFFLINE=1), lê a amostra local."""
    if not OFFLINE:
        try:
            abridor = montar_abridor()
            pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with abridor.open(pedido, timeout=15) as resposta:
                return json.load(resposta)
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    return json.loads((PASTA_DIA / "dados" / amostra).read_text(encoding="utf-8"))


# ── 2. Perguntar o IP ─────────────────────────────────────────────────────
dados = buscar_json(URL_IP, "ipify.json")
ip = dados.get("ip", "?")
print(f"\n🌍 O site enxerga o IP: {ip}")

# ── 3. Interpretar ────────────────────────────────────────────────────────
if ip.startswith(("203.0.113.", "198.51.100.", "192.0.2.")):
    print("   (Esse é um IP de DOCUMENTAÇÃO, da amostra offline. Rode com internet para ver o seu.)")
print("\n🧠 Teste de bancada: rode uma vez sem PROXY_URL e outra com PROXY_URL.")
print("   Se o IP for o mesmo nas duas, o proxy NÃO está funcionando e você está exposto.")
