"""
O que o meu script conta sobre mim? Comparando cabeçalhos HTTP no httpbin.

Carta 33 (rank A) — Jutsu do Disfarce Digital (parte 2)

O que você aprende:
  • que cada pedido HTTP leva cabeçalhos (headers) além do endereço;
  • que o urllib se apresenta como "Python-urllib/3.x", o que denuncia um robô na hora;
  • a enviar um User-Agent e um Accept-Language personalizados;
  • a comparar, lado a lado, o pedido "cru" e o pedido "disfarçado".

O httpbin.org devolve, em JSON, os cabeçalhos que recebeu: é um espelho.

Como rodar (dentro da pasta dia-12-proxies):
    python br/02_o_que_eu_revelo.py
    OSINT_OFFLINE=1 python br/02_o_que_eu_revelo.py
"""

import json
import os
import urllib.request
from pathlib import Path

URL_ESPELHO = "https://httpbin.org/headers"  #@param {type:"string"}
# Um UA de navegador ATUAL e comum. UA velho demais (como o Chrome 45 do original) também chama atenção.
UA_PERSONALIZADO = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"


def cabecalhos_recebidos(cabecalhos_enviados, amostra):
    """Faz o pedido e devolve o dicionário 'headers' que o espelho viu."""
    if not OFFLINE:
        try:
            pedido = urllib.request.Request(URL_ESPELHO, headers=cabecalhos_enviados)
            with urllib.request.urlopen(pedido, timeout=15) as resposta:
                return json.load(resposta)["headers"]
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    return json.loads((PASTA_DIA / "dados" / amostra).read_text(encoding="utf-8"))["headers"]


# ── 1. Pedido "cru": não mandamos nenhum cabeçalho ────────────────────────
# O urllib preenche sozinho o User-Agent com "Python-urllib/<versão>".
padrao = cabecalhos_recebidos({}, "httpbin_headers_padrao.json")

# ── 2. Pedido "disfarçado": UA de navegador + idioma pt-BR ────────────────
personalizado = cabecalhos_recebidos({
    "User-Agent": UA_PERSONALIZADO,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9",
}, "httpbin_headers_personalizado.json")

# ── 3. Tabela comparativa ─────────────────────────────────────────────────
nomes = sorted(set(padrao) | set(personalizado))     # união das chaves dos dois lados
print(f"\n{'Cabeçalho':<17} │ {'Pedido cru':<28} │ Pedido personalizado")
print("─" * 18 + "┼" + "─" * 30 + "┼" + "─" * 40)
for nome in nomes:
    if nome == "X-Amzn-Trace-Id":
        continue          # identificador interno do servidor do httpbin; não vem de nós
    a = padrao.get(nome, "—")[:28]
    b = personalizado.get(nome, "—")
    b = b if len(b) <= 40 else b[:37] + "..."
    print(f"{nome:<17} │ {a:<28} │ {b}")

# ── 4. Diagnóstico ────────────────────────────────────────────────────────
print()
if "python" in padrao.get("User-Agent", "").lower():
    print(f"🚩 Sem cabeçalho, você se anuncia como '{padrao['User-Agent']}'.")
    print("   Qualquer site (e o golpista que olha o log dele) sabe que é um script.")
print("✅ Com o UA personalizado, o pedido se parece com o de um navegador comum.")
print("\n🧠 Mas atenção: disfarçar o UA NÃO esconde o seu IP. Para isso, veja o script 01.")
print("   E no NFA a regra é: em site de instituição, identifique-se com honestidade;")
print("   disfarce é para não alertar o ALVO de uma investigação autorizada.")
