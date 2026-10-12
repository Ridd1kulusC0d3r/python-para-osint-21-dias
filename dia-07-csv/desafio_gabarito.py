"""
Gabarito do Desafio S do Dia 7 — Resumo regional das denúncias.

Junta a planilha de denúncias com a base de municípios do IBGE (cidade padronizada +
mesorregião), calcula vítimas e prejuízo por cidade e por mesorregião, e grava
dois CSVs prontos para o Excel em português, mais um relatório de qualidade
(quantas cidades foram corrigidas e como). Sem internet, usa a amostra do IBGE.
"""

import csv
import difflib
import json
import os
import unicodedata
import urllib.request
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

SIMILARIDADE_MINIMA = 0.85  #@param {type:"number"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"
OFFLINE = os.environ.get("OSINT_OFFLINE") == "1"
APELIDOS = {"bh": "Belo Horizonte", "jf": "Juiz de Fora", "gv": "Governador Valadares"}


def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return " ".join(sem_acento.casefold().split())


def reais_excel(valor):
    """Decimal → '54877,40': vírgula decimal, sem separador de milhar, para o Excel BR somar."""
    return f"{valor:.2f}".replace(".", ",")


def municipios_ibge():
    lista = None
    if not OFFLINE:
        try:
            url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/MG/municipios"
            req = urllib.request.Request(url, headers={"User-Agent": "python-para-osint-21-dias/estudo"})
            with urllib.request.urlopen(req, timeout=30) as resposta:
                lista = json.load(resposta)
        except Exception as erro:
            print(f"⚠️ MODO OFFLINE: a consulta falhou ({erro}). Usando a amostra local.")
    else:
        print("⚠️ MODO OFFLINE: usando a amostra local.")
    if lista is None:
        lista = json.loads((PASTA_DIA / "dados" / "ibge_municipios_mg.json").read_text(encoding="utf-8"))["municipios"]
    base = {}
    for m in lista:
        micro = m.get("microrregiao") or {}                 # null → {}
        meso = (micro.get("mesorregiao") or {}).get("nome", "")
        base[normalizar(m["nome"])] = {"nome": m["nome"], "codigo": m["id"], "mesorregiao": meso or "(sem mesorregião)"}
    return base


base = municipios_ibge()

with open(PASTA_CASO / "denuncias.csv", encoding="utf-8", newline="") as f:
    denuncias = list(csv.DictReader(f, delimiter=";"))

metodos = Counter()
por_cidade = defaultdict(lambda: {"vitimas": 0, "prejuizo": Decimal("0"), "mesorregiao": "", "codigo": ""})
for d in denuncias:
    chave = normalizar(d["cidade"])
    if chave in base:
        metodo = "exato" if base[chave]["nome"] == d["cidade"] else "normalizado"
    elif chave in APELIDOS:
        chave, metodo = normalizar(APELIDOS[chave]), "apelido"
    else:
        parecido = difflib.get_close_matches(chave, base, n=1, cutoff=SIMILARIDADE_MINIMA)
        chave, metodo = (parecido[0], "aproximado") if parecido else (None, "não reconhecida")
    metodos[metodo] += 1
    info = base.get(chave, {"nome": f"?? {d['cidade']}", "codigo": "", "mesorregiao": "(revisar)"})
    linha = por_cidade[info["nome"]]
    linha["vitimas"] += 1
    linha["prejuizo"] += Decimal(d["valor"])
    linha["mesorregiao"], linha["codigo"] = info["mesorregiao"], info["codigo"]

por_meso = defaultdict(lambda: {"vitimas": 0, "prejuizo": Decimal("0"), "cidades": set()})
for cidade, v in por_cidade.items():
    m = por_meso[v["mesorregiao"]]
    m["vitimas"] += v["vitimas"]
    m["prejuizo"] += v["prejuizo"]
    m["cidades"].add(cidade)

SAIDAS.mkdir(exist_ok=True)
with open(SAIDAS / "resumo_por_cidade.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["cidade", "codigo_ibge", "mesorregiao", "vitimas", "prejuizo_reais"])
    for cidade, v in sorted(por_cidade.items(), key=lambda p: -p[1]["prejuizo"]):
        w.writerow([cidade, v["codigo"], v["mesorregiao"], v["vitimas"], reais_excel(v["prejuizo"])])

with open(SAIDAS / "resumo_por_mesorregiao.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["mesorregiao", "cidades", "vitimas", "prejuizo_reais"])
    for meso, v in sorted(por_meso.items(), key=lambda p: -p[1]["prejuizo"]):
        w.writerow([meso, ", ".join(sorted(v["cidades"])), v["vitimas"], reais_excel(v["prejuizo"])])

print("🗺️  Por mesorregião:")
for meso, v in sorted(por_meso.items(), key=lambda p: -p[1]["prejuizo"]):
    print(f"   {meso:<34} {v['vitimas']:>2} vítimas  R$ {reais_excel(v['prejuizo']):>10}")
print("\n🧹 Qualidade da coluna 'cidade':", dict(metodos))
total = sum(Decimal(d["valor"]) for d in denuncias)
conferido = sum(v["prejuizo"] for v in por_cidade.values())
print("✅ Total confere com a planilha." if total == conferido else "🚩 Total NÃO confere!")
print("💾 saidas/resumo_por_cidade.csv e saidas/resumo_por_mesorregiao.csv gravados.")
