"""
Gabarito do Desafio S do Dia 5 — Verificador de CEPs em lote com fonte reserva.

Recebe vários CEPs, consulta a BrasilAPI e, se ela falhar, pergunta ao ViaCEP.
Marca CEPs inexistentes, mostra de qual fonte veio cada resposta e grava
saidas/ceps_verificados.csv. Sem internet (ou com OSINT_OFFLINE=1), usa as amostras.
"""

import csv
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

CEPS = "30130-010, 01001-000, 99999-999, 1234"  #@param {type:"string"}
PAUSA_SEGUNDOS = 1  #@param {type:"number"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"

# Amostras locais por CEP (só existem para alguns; os outros ficam "sem dados" offline)
AMOSTRAS_BRASILAPI = {"30130010": "brasilapi_cep_30130010.json"}
AMOSTRAS_VIACEP = {"30130010": "viacep_30130010.json", "01001000": "viacep_01001000.json",
                   "99999999": "viacep_inexistente.json"}


def baixar(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
    with urllib.request.urlopen(pedido, timeout=15) as resposta:
        return json.load(resposta)


def amostra(nome):
    return json.loads((PASTA_DIA / "dados" / nome).read_text(encoding="utf-8"))


def via_brasilapi(cep):
    """Devolve (linha, situação). Situação: 'ok', 'inexistente' ou 'falhou'."""
    if OFFLINE:
        if cep in AMOSTRAS_BRASILAPI:
            d = amostra(AMOSTRAS_BRASILAPI[cep])
        else:
            return None, "falhou"
    else:
        try:
            d = baixar(f"https://brasilapi.com.br/api/cep/v2/{cep}")
        except urllib.error.HTTPError as erro:
            return None, "inexistente" if erro.code == 404 else "falhou"
        except Exception:
            return None, "falhou"
    return {"logradouro": d.get("street", ""), "bairro": d.get("neighborhood", ""),
            "cidade": d.get("city", ""), "uf": d.get("state", "")}, "ok"


def via_viacep(cep):
    if OFFLINE:
        if cep not in AMOSTRAS_VIACEP:
            return None, "falhou"
        d = amostra(AMOSTRAS_VIACEP[cep])
    else:
        try:
            d = baixar(f"https://viacep.com.br/ws/{cep}/json/")
        except Exception:
            return None, "falhou"
    if str(d.get("erro", "")).lower() == "true":      # "true" (texto) ou true (booleano)
        return None, "inexistente"
    return {"logradouro": d.get("logradouro", ""), "bairro": d.get("bairro", ""),
            "cidade": d.get("localidade", ""), "uf": d.get("uf", "")}, "ok"


if OFFLINE:
    print("⚠️ MODO OFFLINE: usando as amostras locais.")

linhas = []
for bruto in [c.strip() for c in CEPS.split(",") if c.strip()]:
    cep = "".join(ch for ch in bruto if ch.isdigit())
    linha = {"cep_digitado": bruto, "cep": cep, "fonte": "", "situacao": "",
             "logradouro": "", "bairro": "", "cidade": "", "uf": ""}
    if len(cep) != 8:
        linha["situacao"] = "formato inválido (não consultado)"   # não gasta consulta à toa
    else:
        dados, situacao = via_brasilapi(cep)
        fonte = "BrasilAPI"
        if situacao != "ok":                                       # fonte reserva
            dados, situacao = via_viacep(cep)
            fonte = "ViaCEP"
        linha["fonte"] = fonte if situacao != "falhou" else ""
        linha["situacao"] = {"ok": "encontrado", "inexistente": "🚩 CEP inexistente",
                             "falhou": "sem resposta"}[situacao]
        if dados:
            linha.update(dados)
        if not OFFLINE:
            time.sleep(PAUSA_SEGUNDOS)                             # educação com a API
    linhas.append(linha)
    print(f"{bruto:<11} {linha['situacao']:<34} {linha['fonte']:<10} {linha['logradouro']} {linha['cidade']}")

SAIDAS = PASTA_DIA / "saidas"
SAIDAS.mkdir(exist_ok=True)
with open(SAIDAS / "ceps_verificados.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=list(linhas[0]), delimiter=";")
    escritor.writeheader()
    escritor.writerows(linhas)
print("\n💾 saidas/ceps_verificados.csv gravado.")
