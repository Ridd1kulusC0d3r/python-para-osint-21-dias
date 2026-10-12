"""
Consultar um CEP na BrasilAPI (uma API brasileira, gratuita e sem cadastro).

Carta 26 (rank B) — Jutsu do Mensageiro HTTP (parte 2)

O que você aprende:
  • a consultar uma API pública brasileira só com a biblioteca padrão;
  • a ler campos aninhados (location → coordinates → latitude);
  • a limpar a entrada (tirar ponto e traço do CEP) antes de montar a URL;
  • a usar .get() para não quebrar quando um campo não vier.

Como rodar (dentro da pasta dia-05-http-e-apis):
    python br/02_cep_brasilapi.py
    OSINT_OFFLINE=1 python br/02_cep_brasilapi.py
"""

import json
import os
import urllib.request
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
CEP = "30130-010"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"


def buscar_json(url, amostra):
    """Baixa um JSON da internet; se falhar (ou OFFLINE=1), lê a amostra local."""
    if not OFFLINE:
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(pedido, timeout=15) as resposta:
                return json.load(resposta)
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    return json.loads((PASTA_DIA / "dados" / amostra).read_text(encoding="utf-8"))


# ── 1. Limpar o CEP: só os 8 dígitos ──────────────────────────────────────
# "30130-010" → "30130010". Isso evita URL errada e também protege contra
# alguém colar texto estranho no parâmetro.
cep = "".join(c for c in CEP if c.isdigit())
if len(cep) != 8:
    raise SystemExit(f"CEP precisa ter 8 dígitos; recebi {CEP!r}")

# ── 2. Consultar ──────────────────────────────────────────────────────────
# A v2 da BrasilAPI pergunta a vários provedores e devolve o primeiro que responder.
url = f"https://brasilapi.com.br/api/cep/v2/{cep}"
print(f"🌐 GET {url}\n")
dados = buscar_json(url, "brasilapi_cep_30130010.json")

# ── 3. Mostrar os campos principais ───────────────────────────────────────
# Os nomes dos campos estão em inglês (é o padrão da BrasilAPI).
print(f"📮 CEP:        {dados.get('cep')}")
print(f"🛣️  Logradouro: {dados.get('street') or '(sem logradouro: CEP geral da cidade?)'}")
print(f"🏘️  Bairro:     {dados.get('neighborhood')}")
print(f"🏙️  Cidade/UF:  {dados.get('city')}/{dados.get('state')}")
print(f"🛰️  Fonte:      {dados.get('service')}  ← qual provedor respondeu de verdade")

# ── 4. Campo aninhado: coordenadas ────────────────────────────────────────
# location é um dicionário que tem outro dicionário dentro (coordinates).
# Encadeamos .get(..., {}) para não quebrar se algum nível estiver vazio.
coordenadas = dados.get("location", {}).get("coordinates", {})
lat, lon = coordenadas.get("latitude"), coordenadas.get("longitude")
if lat and lon:
    print(f"📍 Coordenadas: {lat}, {lon}")
    print(f"🗺️  Ver no mapa: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}")
else:
    print("📍 Coordenadas: não vieram (acontece com vários CEPs; não é erro).")
