"""
Vários termos, vários municípios: guardar os achados do Querido Diário num CSV.

Carta 30 (rank B) — Jutsu do Diário Oficial (parte 2)

O que você aprende:
  • a repetir a mesma consulta para uma lista de termos × municípios (laço duplo);
  • a fazer uma pausa entre pedidos (educação com a API pública);
  • a gravar os resultados num CSV com a data da coleta (o "ddg_search_to_csv" do original, em versão BR);
  • a tirar resultados repetidos (o mesmo diário pode aparecer para dois termos).

Como rodar (dentro da pasta dia-09-resultados-de-busca):
    python br/02_querido_diario_csv.py
    OSINT_OFFLINE=1 python br/02_querido_diario_csv.py
"""

import csv
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
TERMOS = "PIX, golpe, comércio eletrônico"  #@param {type:"string"}
# Códigos IBGE separados por vírgula: Belo Horizonte, Contagem, Betim
MUNICIPIOS = "3106200, 3118601, 3106705"  #@param {type:"string"}
DESDE = "2025-10-01"  #@param {type:"date"}
POR_CONSULTA = 10  #@param {type:"integer"}
PAUSA_SEGUNDOS = 1.5  #@param {type:"number"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"
SAIDAS = PASTA_DIA / "saidas"

try:
    from zoneinfo import ZoneInfo
    FUSO_BR = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO_BR = timezone(timedelta(hours=-3))


def consultar(termo, codigo):
    """Uma consulta ao Querido Diário. Devolve a lista 'gazettes' (ou a amostra)."""
    parametros = {"querystring": termo, "territory_ids": codigo, "published_since": DESDE,
                  "size": POR_CONSULTA, "excerpt_size": 200, "number_of_excerpts": 1}
    url = "https://api.queridodiario.ok.org.br/gazettes?" + urllib.parse.urlencode(parametros)
    pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
    with urllib.request.urlopen(pedido, timeout=30) as resposta:
        return json.load(resposta).get("gazettes", [])


termos = [t.strip() for t in TERMOS.split(",") if t.strip()]
codigos = [c.strip() for c in MUNICIPIOS.split(",") if c.strip()]
coletado_em = datetime.now(FUSO_BR).isoformat(timespec="seconds")

# ── 1. Coletar ────────────────────────────────────────────────────────────
linhas = {}             # chave = (url, termo) → evita duplicar a mesma linha
usar_amostra = OFFLINE
if OFFLINE:
    print("⚠️ MODO OFFLINE: usando a amostra local.")

for termo in termos:
    for codigo in codigos:
        diarios = None
        if not usar_amostra:
            try:
                diarios = consultar(termo, codigo)
                time.sleep(PAUSA_SEGUNDOS)          # não sobrecarregar um serviço público e gratuito
            except Exception as erro:
                print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
                usar_amostra = True                 # caiu uma vez? usamos a amostra no resto
        if diarios is None:
            amostra = json.loads((PASTA_DIA / "dados" / "querido_diario_bh.json").read_text(encoding="utf-8"))
            # A amostra só tem BH; filtramos pelo município e pelo termo para simular a busca.
            diarios = [g for g in amostra["gazettes"] if g.get("territory_id") == codigo
                       and any(termo.casefold() in e.casefold() for e in g.get("excerpts", []))]
        print(f"🔎 {termo!r:<24} em {codigo}: {len(diarios)} diário(s)")
        for g in diarios:
            linhas[(g.get("url"), termo)] = {
                "termo": termo,
                "codigo_ibge": g.get("territory_id", codigo),
                "municipio": g.get("territory_name", ""),
                "uf": g.get("state_code", ""),
                "data": g.get("date", ""),
                "edicao": g.get("edition") or "",
                "extra": "sim" if g.get("is_extra_edition") else "não",
                "trecho": " ".join(" ".join(g.get("excerpts", [])).split())[:300],
                "url": g.get("url", ""),
                "coletado_em": coletado_em,          # quando NÓS vimos (importante para a prova)
            }

# ── 2. Gravar ─────────────────────────────────────────────────────────────
SAIDAS.mkdir(exist_ok=True)
destino = SAIDAS / "querido_diario_resultados.csv"
campos = ["termo", "codigo_ibge", "municipio", "uf", "data", "edicao", "extra", "trecho", "url", "coletado_em"]
with open(destino, "w", encoding="utf-8-sig", newline="") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
    escritor.writeheader()
    # Ordenamos por data (mais recente primeiro) para facilitar a leitura.
    escritor.writerows(sorted(linhas.values(), key=lambda l: l["data"], reverse=True))
print(f"\n💾 {len(linhas)} linha(s) em {destino.relative_to(PASTA_DIA)}")
