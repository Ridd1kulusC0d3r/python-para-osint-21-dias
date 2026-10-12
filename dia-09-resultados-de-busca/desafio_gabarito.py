"""
Gabarito do Desafio S do Dia 9 — Vigia do Diário Oficial.

Consulta o Querido Diário para uma lista de termos em um município, compara com
o que já foi visto nas execuções anteriores (saidas/vigia_estado.json) e mostra
SÓ as publicações novas. Grava um relatório HTML com links e trechos.
Sem internet (ou com OSINT_OFFLINE=1), usa a amostra local.
"""

import html
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

TERMOS = "PIX, Black Friday, consumidor"  #@param {type:"string"}
CODIGO_IBGE = "3106200"  #@param {type:"string"}
DIAS_PARA_TRAS = 120  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
SAIDAS = PASTA_DIA / "saidas"
ESTADO = SAIDAS / "vigia_estado.json"
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"

try:
    from zoneinfo import ZoneInfo
    FUSO_BR = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO_BR = timezone(timedelta(hours=-3))

agora = datetime.now(FUSO_BR)
desde = (agora - timedelta(days=DIAS_PARA_TRAS)).date().isoformat()


def buscar(termo):
    if not OFFLINE:
        try:
            q = urllib.parse.urlencode({"querystring": termo, "territory_ids": CODIGO_IBGE, "published_since": desde,
                                        "size": 20, "excerpt_size": 200, "number_of_excerpts": 1})
            req = urllib.request.Request("https://api.queridodiario.ok.org.br/gazettes?" + q,
                                         headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(req, timeout=30) as resposta:
                dados = json.load(resposta)
            time.sleep(1)
            return dados.get("gazettes", [])
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    amostra = json.loads((PASTA_DIA / "dados" / "querido_diario_bh.json").read_text(encoding="utf-8"))
    # A amostra é de 2025: no modo offline ignoramos o filtro de data e filtramos só pelo termo.
    return [g for g in amostra["gazettes"] if g.get("territory_id") == CODIGO_IBGE
            and any(termo.casefold() in e.casefold() for e in g.get("excerpts", []))]


if OFFLINE:
    print("⚠️ MODO OFFLINE: usando a amostra local.")

# Estado anterior: conjunto de "impressões digitais" (url + termo) já vistas
try:
    vistos = set(json.loads(ESTADO.read_text(encoding="utf-8"))["vistos"])
except (FileNotFoundError, KeyError, json.JSONDecodeError):
    vistos = set()
primeira_vez = not vistos

novidades = []
for termo in [t.strip() for t in TERMOS.split(",") if t.strip()]:
    for g in buscar(termo):
        chave = f"{g.get('url')}|{termo}"
        if chave not in vistos:
            vistos.add(chave)
            novidades.append({"termo": termo, "data": g.get("date", ""), "url": g.get("url", ""),
                              "municipio": g.get("territory_name", ""),
                              "trecho": " ".join(" ".join(g.get("excerpts", [])).split())[:300]})

novidades.sort(key=lambda n: n["data"], reverse=True)
print(f"{'🆕 Primeira execução' if primeira_vez else '🔁 Execução de acompanhamento'}: "
      f"{len(novidades)} publicação(ões) nova(s).")
for n in novidades:
    print(f"   {n['data']}  [{n['termo']}]  {n['url']}")

SAIDAS.mkdir(exist_ok=True)
ESTADO.write_text(json.dumps({"atualizado_em": agora.isoformat(timespec="seconds"),
                              "vistos": sorted(vistos)}, indent=2, ensure_ascii=False), encoding="utf-8")
itens = "".join(
    f"<li><b>{html.escape(n['data'])}</b> · {html.escape(n['termo'])} · {html.escape(n['municipio'])}<br>"
    f"<small>{html.escape(n['trecho'])}</small><br>"
    f"<a href='{html.escape(n['url'], quote=True)}' target='_blank' rel='noopener noreferrer'>abrir diário</a></li>"
    for n in novidades) or "<li>Nenhuma novidade desde a última execução.</li>"
(SAIDAS / "vigia_novidades.html").write_text(
    f"<!doctype html><html lang='pt-BR'><meta charset='utf-8'><title>Vigia do Diário Oficial</title>"
    f"<body style='font-family:sans-serif;max-width:800px;margin:auto'><h1>Vigia do Diário Oficial</h1>"
    f"<p>Município {html.escape(CODIGO_IBGE)} · gerado em {agora:%d/%m/%Y %H:%M}</p><ul>{itens}</ul></body></html>",
    encoding="utf-8")
print("💾 saidas/vigia_estado.json e saidas/vigia_novidades.html gravados. Rode de novo: zero novidades.")
