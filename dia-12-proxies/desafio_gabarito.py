"""
Gabarito do Desafio S do Dia 12 — Classificador de proxies (vivo? vaza o meu IP?).

Para cada proxy da lista, faz um pedido a https://httpbin.org/get através dele e
classifica em: ⛔ morto · 🚩 transparente (vaza seu IP) · 🟡 anônimo (avisa que é
proxy) · ✅ elite (não vaza nada). Mede a latência e grava saidas/proxies.csv.
Sem internet (ou com OSINT_OFFLINE=1), usa resultados simulados de dados/.
"""

import csv
import json
import os
import time
import urllib.request
from pathlib import Path

ARQUIVO_LISTA = "dados/proxies_teste.txt"  #@param {type:"string"}
URL_TESTE = "https://httpbin.org/get"  #@param {type:"string"}
TIMEOUT = 8  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"
UA = "python-para-osint-21-dias/estudo"

# Cabeçalhos que denunciam a presença de um proxy no caminho.
DEDO_DURO = ("Via", "X-Forwarded-For", "Forwarded", "X-Real-Ip", "Proxy-Connection")


def pedir(proxy=None):
    """Faz o pedido (direto ou pelo proxy). Devolve (json, latência em ms)."""
    manipulador = urllib.request.ProxyHandler({"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else {})
    abridor = urllib.request.build_opener(manipulador)
    inicio = time.perf_counter()
    with abridor.open(urllib.request.Request(URL_TESTE, headers={"User-Agent": UA}), timeout=TIMEOUT) as r:
        dados = json.load(r)
    return dados, round((time.perf_counter() - inicio) * 1000)


def classificar(resposta, ip_real):
    origem = resposta.get("origin", "")
    cabecalhos = {k.title(): v for k, v in resposta.get("headers", {}).items()}
    if ip_real and (ip_real in origem or ip_real in " ".join(cabecalhos.values())):
        return "🚩 transparente (vaza seu IP)"
    if any(nome.title() in cabecalhos for nome in DEDO_DURO):
        return "🟡 anônimo (avisa que é proxy)"
    return "✅ elite"


# ── 1. Ler a lista (ignorando comentários e linhas vazias) ────────────────
linhas = (PASTA_DIA / ARQUIVO_LISTA).read_text(encoding="utf-8").splitlines()
proxies = [l.strip() for l in linhas if l.strip() and not l.startswith("#")]

# ── 2. Descobrir o IP real (sem proxy) e testar cada proxy ────────────────
resultados = {}
if not OFFLINE:
    try:
        ip_real = pedir()[0]["origin"]
        for proxy in proxies:
            try:
                resposta, ms = pedir(proxy)
                resultados[proxy] = {"latencia_ms": ms, "resposta": resposta}
            except Exception as erro:              # um proxy ruim não derruba o laço
                resultados[proxy] = {"erro": str(erro)[:60]}
    except Exception as erro:
        print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
        OFFLINE = True
else:
    print("⚠️ MODO OFFLINE: usando a amostra local.")
if OFFLINE:
    amostra = json.loads((PASTA_DIA / "dados" / "teste_proxies_amostra.json").read_text(encoding="utf-8"))
    ip_real, resultados = amostra["ip_real"], amostra["resultados"]

# ── 3. Classificar e mostrar ──────────────────────────────────────────────
print(f"\n🏠 Seu IP real: {ip_real}\n")
tabela = []
for proxy in proxies:
    r = resultados.get(proxy, {"erro": "não testado"})
    if "erro" in r:
        tabela.append({"proxy": proxy, "classe": "⛔ morto", "latencia_ms": "", "detalhe": r["erro"]})
    else:
        tabela.append({"proxy": proxy, "classe": classificar(r["resposta"], ip_real),
                       "latencia_ms": r["latencia_ms"], "detalhe": r["resposta"].get("origin", "")})

# Ordena: elite primeiro, depois os mais rápidos.
ordem = {"✅": 0, "🟡": 1, "🚩": 2, "⛔": 3}
tabela.sort(key=lambda t: (ordem[t["classe"][0]], t["latencia_ms"] or 10**9))
for t in tabela:
    print(f"  {t['proxy']:<22} {t['classe']:<32} {str(t['latencia_ms']):>6} ms  {t['detalhe']}")

saidas = PASTA_DIA / "saidas"
saidas.mkdir(exist_ok=True)
with open(saidas / "proxies.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=["proxy", "classe", "latencia_ms", "detalhe"], delimiter=";")
    escritor.writeheader()
    escritor.writerows(tabela)
print("\n💾 saidas/proxies.csv gravado.")
print("🧠 'Elite' só quer dizer que o SITE não te vê. O dono do proxy continua vendo tudo.")
