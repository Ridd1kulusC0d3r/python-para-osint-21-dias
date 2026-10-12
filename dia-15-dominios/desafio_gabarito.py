"""
Gabarito do Desafio S do Dia 15 — Radar de domínios recém-nascidos.

Lê uma lista de domínios, consulta o RDAP de cada um (descobrindo o servidor pelo
bootstrap da IANA) e grava radar_dominios.csv com idade e um alerta.
Sem internet (ou com OSINT_OFFLINE=1), usa as amostras locais.
"""

import csv
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DOMINIOS = "registro.br, nic.br, megaoferta-brasil.example"  #@param {type:"string"}
LIMITE_DIAS = 90  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"

# Amostras locais por domínio (usadas quando não há internet)
AMOSTRAS = {
    "registro.br": PASTA_DIA / "dados" / "rdap_registro_br.json",
    "megaoferta-brasil.example": PASTA_CASO / "rdap_megaoferta.json",
}


def baixar(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
    with urllib.request.urlopen(pedido, timeout=15) as resposta:
        return json.load(resposta)


def servidores_rdap():
    """Dicionário tld → url do servidor RDAP."""
    try:
        if OFFLINE:
            raise RuntimeError("offline")
        bootstrap = baixar("https://data.iana.org/rdap/dns.json")
    except Exception:
        bootstrap = json.loads((PASTA_DIA / "dados" / "iana_rdap_dns.json").read_text(encoding="utf-8"))
    return {tld: urls[0] for tlds, urls in bootstrap["services"] for tld in tlds}


def consultar(dominio, mapa):
    tld = dominio.rsplit(".", 1)[-1]
    if not OFFLINE and tld in mapa:
        try:
            return baixar(mapa[tld].rstrip("/") + "/domain/" + dominio), "ao vivo"
        except Exception:
            pass
    if dominio in AMOSTRAS:
        return json.loads(AMOSTRAS[dominio].read_text(encoding="utf-8")), "amostra"
    return None, "sem dados"


mapa = servidores_rdap()
linhas = []
for dominio in [d.strip() for d in DOMINIOS.split(",") if d.strip()]:
    dados, origem = consultar(dominio, mapa)
    linha = {"dominio": dominio, "origem": origem, "criado_em": "", "idade_dias": "",
             "nameservers": "", "alerta": ""}
    if dados:
        eventos = {e["eventAction"]: e["eventDate"] for e in dados.get("events", [])}
        if "registration" in eventos:
            criado = datetime.fromisoformat(eventos["registration"].replace("Z", "+00:00"))
            # Para a amostra fictícia, medimos a idade na data da 1ª denúncia (12/10/2025)
            referencia = datetime(2025, 10, 12, tzinfo=timezone.utc) if dominio.endswith(".example") \
                else datetime.now(timezone.utc)
            idade = (referencia - criado).days
            linha.update(criado_em=criado.date().isoformat(), idade_dias=idade,
                         alerta="🚩 recém-nascido" if idade < LIMITE_DIAS else "ok")
        linha["nameservers"] = " ".join(ns.get("ldhName", "") for ns in dados.get("nameservers", []))
    linhas.append(linha)
    print(f"{dominio:<28} {origem:<9} {linha['idade_dias']!s:>6} dias  {linha['alerta']}")

SAIDAS = PASTA_DIA / "saidas"
SAIDAS.mkdir(exist_ok=True)
with open(SAIDAS / "radar_dominios.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=list(linhas[0]), delimiter=";")
    escritor.writeheader()
    escritor.writerows(linhas)
print("\n💾 saidas/radar_dominios.csv gravado (abre direto no Excel em pt-BR).")
