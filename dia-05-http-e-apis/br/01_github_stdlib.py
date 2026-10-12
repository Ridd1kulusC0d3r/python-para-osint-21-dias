"""
O mesmo pedido do original (busca de usuários no GitHub), só com a biblioteca padrão.

Carta 26 (rank B) — Jutsu do Mensageiro HTTP

O que você aprende:
  • a fazer um GET com urllib.request (vem com o Python, sem pip install);
  • a ler as três partes de uma resposta HTTP: status, cabeçalhos e corpo;
  • a ler os cabeçalhos de limite de uso (rate limit) que o GitHub manda;
  • a montar parâmetros de URL com urllib.parse.urlencode (acentos e espaços seguros).

Como rodar (dentro da pasta dia-05-http-e-apis):
    python br/01_github_stdlib.py
    OSINT_OFFLINE=1 python br/01_github_stdlib.py   # sem internet, usa dados/
"""

import json                 # transformar o texto JSON em dicionário Python
import os                   # ler a variável de ambiente OSINT_OFFLINE
import urllib.parse         # montar a parte "?q=..." da URL com segurança
import urllib.request       # fazer o pedido HTTP
from datetime import datetime, timedelta, timezone  # converter o horário do reset
from pathlib import Path    # montar caminhos de arquivo

# ── Parâmetros (no Colab viram um formulário) ─────────────────────────────
BUSCA = "osint"  #@param {type:"string"}
QUANTOS = 5  #@param {type:"integer"}

# ── Pastas e modo offline ─────────────────────────────────────────────────
PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"

# Horário de Brasília. No Windows pode faltar o banco de fusos (tzdata): usamos -3h fixo.
try:
    from zoneinfo import ZoneInfo
    FUSO_BR = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO_BR = timezone(timedelta(hours=-3))


def pedir(url):
    """Faz um GET e devolve (status, cabeçalhos, corpo_em_dicionário)."""
    pedido = urllib.request.Request(url, headers={
        # O GitHub EXIGE um User-Agent. Sem ele, a API recusa o pedido.
        "User-Agent": "python-para-osint-21-dias/estudo",
        # Pedimos explicitamente a versão JSON da API.
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(pedido, timeout=15) as resposta:
        status = resposta.status                       # 200 = deu certo
        cabecalhos = {k.lower(): v for k, v in resposta.headers.items()}
        corpo = json.load(resposta)                    # lê e converte o JSON
    return status, cabecalhos, corpo


# ── 1. Montar a URL ───────────────────────────────────────────────────────
# urlencode cuida de espaços e acentos: "são paulo" vira "s%C3%A3o+paulo".
parametros = urllib.parse.urlencode({"q": BUSCA, "per_page": QUANTOS})
url = "https://api.github.com/search/users?" + parametros
print(f"🌐 GET {url}\n")

# ── 2. Fazer o pedido (ou usar a amostra) ─────────────────────────────────
resultado = None
if not OFFLINE:
    try:
        resultado = pedir(url)
    except Exception as erro:
        print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
else:
    print("⚠️ MODO OFFLINE: usando a amostra local.")

if resultado is None:
    amostra = json.loads((PASTA_DIA / "dados" / "github_search_users.json").read_text(encoding="utf-8"))
    # A amostra guarda status e cabeçalhos em campos extras que começam com "_".
    resultado = (amostra["_status"], amostra["_cabecalhos"], amostra)

status, cabecalhos, corpo = resultado

# ── 3. Status: o "deu certo?" do HTTP ─────────────────────────────────────
# 2xx = sucesso · 3xx = redirecionamento · 4xx = erro seu · 5xx = erro do servidor
print(f"📶 Status HTTP: {status}")

# ── 4. Cabeçalhos de rate limit ───────────────────────────────────────────
# O GitHub conta quantos pedidos você fez. A busca tem limite bem menor que o resto.
print("\n⏱️  Limite de uso (rate limit):")
for nome in ["x-ratelimit-resource", "x-ratelimit-limit", "x-ratelimit-used", "x-ratelimit-remaining"]:
    print(f"   {nome:<22} = {cabecalhos.get(nome, '(não veio)')}")

reset = cabecalhos.get("x-ratelimit-reset")
if reset:
    # O reset vem como "timestamp Unix" (segundos desde 01/01/1970, em UTC).
    quando = datetime.fromtimestamp(int(reset), tz=timezone.utc).astimezone(FUSO_BR)
    print(f"   o contador zera em    = {quando:%d/%m/%Y %H:%M} (horário de Brasília)")

# ── 5. Corpo: o JSON com os resultados ────────────────────────────────────
print(f"\n🔢 total_count = {corpo.get('total_count')}")
for usuario in corpo.get("items", [])[:QUANTOS]:
    print(f"   👤 {usuario.get('login'):<22} {usuario.get('type', ''):<13} {usuario.get('html_url')}")

print("\n💡 Compare com original/api_request.py: lá o requests fez tudo isso escondido.")
