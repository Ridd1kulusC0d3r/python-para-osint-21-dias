"""
Buscar palavras nos Diários Oficiais dos municípios com a API do Querido Diário.

Carta 30 (rank B) — Jutsu do Diário Oficial

O que você aprende:
  • a montar uma URL com vários parâmetros (querystring, territory_ids, datas, tamanhos);
  • a ler uma resposta paginada: total_gazettes (quantos existem) × gazettes (quantos vieram);
  • a tratar a resposta com .get e, se a estrutura mudar, mostrar as chaves recebidas;
  • que Diário Oficial é fonte aberta OFICIAL: contratos, nomeações, licenças, sanções.

Como rodar (dentro da pasta dia-09-resultados-de-busca):
    python br/01_querido_diario.py
    OSINT_OFFLINE=1 python br/01_querido_diario.py
"""

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
TERMO = "PIX"  #@param {type:"string"}
CODIGO_IBGE = "3106200"  #@param {type:"string"}
DESDE = "2025-10-01"  #@param {type:"date"}
ATE = "2025-12-31"  #@param {type:"date"}
QUANTOS = 5  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"


def buscar_json(url, amostra):
    """Baixa um JSON da internet; se falhar (ou OFFLINE=1), lê a amostra local."""
    if not OFFLINE:
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(pedido, timeout=30) as resposta:
                return json.load(resposta)
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    return json.loads((PASTA_DIA / "dados" / amostra).read_text(encoding="utf-8"))


# ── 1. Montar a URL ───────────────────────────────────────────────────────
# 3106200 é o código IBGE de Belo Horizonte (o mesmo do Dia 7). Cada parâmetro:
#   querystring        → o que procurar no texto dos diários
#   territory_ids      → em qual município (código IBGE)
#   published_since/until → período (AAAA-MM-DD)
#   size               → quantos diários devolver nesta página
#   excerpt_size       → tamanho (em caracteres) de cada trecho com a palavra
#   number_of_excerpts → quantos trechos por diário
parametros = {
    "querystring": TERMO,
    "territory_ids": CODIGO_IBGE,
    "published_since": DESDE,
    "published_until": ATE,
    "size": QUANTOS,
    "excerpt_size": 250,
    "number_of_excerpts": 1,
}
url = "https://api.queridodiario.ok.org.br/gazettes?" + urllib.parse.urlencode(parametros)
print(f"🌐 GET {url}\n")

resposta = buscar_json(url, "querido_diario_bh.json")

# ── 2. A estrutura veio como esperado? ────────────────────────────────────
# Esperamos {"total_gazettes": N, "gazettes": [...]}. APIs mudam; se mudar, avisamos.
if not isinstance(resposta, dict) or "gazettes" not in resposta:
    chaves = list(resposta) if isinstance(resposta, dict) else type(resposta).__name__
    raise SystemExit(f"🤔 Estrutura diferente da esperada. Chaves recebidas: {chaves}")

diarios = resposta.get("gazettes", [])
total = resposta.get("total_gazettes", len(diarios))
print(f"📰 {total} diário(s) com '{TERMO}' no período · mostrando {len(diarios)}")
if total == 0:
    print("   Nada encontrado. Confira o termo, o período e se o município está coberto pelo projeto.")

# ── 3. Cada diário ────────────────────────────────────────────────────────
for diario in diarios:
    extra = " (edição extra)" if diario.get("is_extra_edition") else ""
    print(f"\n🗓️  {diario.get('date')} · {diario.get('territory_name')}/{diario.get('state_code')}"
          f" · edição {diario.get('edition') or '?'}{extra}")
    print(f"   📄 {diario.get('url')}")
    for trecho in diario.get("excerpts", []):
        # Os trechos vêm com quebras de linha do PDF; juntamos tudo numa linha só.
        print(f"   💬 {' '.join(trecho.split())[:250]}")

# ── 4. Paginação ──────────────────────────────────────────────────────────
if total > len(diarios):
    print(f"\n➡️  Há mais {total - len(diarios)} resultado(s). Peça a próxima página com offset={len(diarios)}.")
