"""
Wayback Machine sem instalar nada: a API CDX do Internet Archive.

Carta 40 (rank A) — Jutsu da Linha do Tempo (parte 2)

O que você aprende:
  • a perguntar à API CDX "quais capturas existem desta página?";
  • a ler a resposta JSON, em que a PRIMEIRA linha é o cabeçalho;
  • a converter o timestamp AAAAMMDDhhmmss em data de verdade;
  • a contar capturas por ano e a montar o link para abrir cada cópia arquivada;
  • a perceber mudanças de conteúdo pelo "digest" e pelo "length".

Como rodar (dentro da pasta dia-19-wayback-e-datas):
    python br/02_wayback_cdx.py
    OSINT_OFFLINE=1 python br/02_wayback_cdx.py
"""

import json
import os
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
URL_ALVO = "gov.br"  #@param {type:"string"}
LIMITE = 200  #@param {type:"integer"}
APENAS_STATUS_200 = False  #@param {type:"boolean"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"


def buscar_json(url, amostra):
    """Baixa um JSON da internet; se falhar (ou OFFLINE=1), lê a amostra local."""
    if not OFFLINE:
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(pedido, timeout=30) as resposta:
                texto = resposta.read().decode("utf-8")
                # Sem nenhuma captura, a API devolve corpo vazio (e não uma lista vazia).
                return json.loads(texto) if texto.strip() else []
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    print("   (amostra ILUSTRATIVA no formato real da API CDX: datas e tamanhos não são os verdadeiros)")
    return json.loads((PASTA_DIA / "dados" / amostra).read_text(encoding="utf-8"))


# ── 1. Montar a consulta ──────────────────────────────────────────────────
# A API CDX aceita parâmetros na URL. Os principais:
#   url=      página (ou domínio) consultado
#   output=json   resposta em JSON (o padrão é texto separado por espaços)
#   limit=    quantas linhas no máximo
#   filter=statuscode:200   só capturas que deram certo
#   collapse=digest         esconde capturas idênticas seguidas (mesmo conteúdo)
parametros = {"url": URL_ALVO, "output": "json", "limit": LIMITE}
if APENAS_STATUS_200:
    parametros["filter"] = "statuscode:200"
url = "https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(parametros)
print(f"🔎 {url}\n")

linhas = buscar_json(url, "wayback_cdx_gov_br.json")
if len(linhas) < 2:
    raise SystemExit("Nenhuma captura encontrada para esse endereço.")

# ── 2. Primeira linha = cabeçalho ─────────────────────────────────────────
cabecalho, dados = linhas[0], linhas[1:]
print(f"🧾 Colunas: {cabecalho}")
# zip(cabecalho, linha) casa cada nome de coluna com o valor: vira um dicionário.
capturas = [dict(zip(cabecalho, linha)) for linha in dados]
print(f"📸 {len(capturas)} capturas recebidas.\n")


def quando(timestamp):
    """'20251128233001' → datetime em UTC (a Wayback registra tudo em UTC)."""
    return datetime.strptime(timestamp, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)


# ── 3. Primeira, última e contagem por ano ────────────────────────────────
primeira, ultima = capturas[0], capturas[-1]
print(f"🥇 Primeira captura: {quando(primeira['timestamp']):%d/%m/%Y %H:%M} UTC  (status {primeira['statuscode']})")
print(f"🕒 Última captura:   {quando(ultima['timestamp']):%d/%m/%Y %H:%M} UTC  (status {ultima['statuscode']})")

por_ano = Counter(c["timestamp"][:4] for c in capturas)       # os 4 primeiros dígitos = ano
print("\n📊 Capturas por ano:")
maior = max(por_ano.values())
for ano in sorted(por_ano):
    print(f"   {ano} {'▇' * round(por_ano[ano] / maior * 30):<30} {por_ano[ano]}")

# ── 4. Status e mudanças de conteúdo ──────────────────────────────────────
print(f"\n🚦 Status HTTP: {dict(Counter(c['statuscode'] for c in capturas))}")
# digest = impressão digital (SHA-1, em base32) do conteúdo. Digest diferente = página mudou.
versoes = len({c["digest"] for c in capturas})
print(f"🧬 Versões diferentes de conteúdo (digests distintos): {versoes}")

# ── 5. Links para abrir as cópias ─────────────────────────────────────────
# https://web.archive.org/web/<timestamp>/<url original>  → a página como estava naquele dia.
# Acrescentar "id_" ao timestamp traz o HTML ORIGINAL, sem a barra de navegação da Wayback.
print("\n🔗 Abra as cópias (as 3 últimas):")
for c in capturas[-3:]:
    print(f"   https://web.archive.org/web/{c['timestamp']}/{c['original']}")
print(f"   HTML cru: https://web.archive.org/web/{ultima['timestamp']}id_/{ultima['original']}")
