"""
Gabarito do Desafio S do Dia 19 — Que vitrine a vítima viu?

Para cada denúncia, descobre qual captura da Wayback Machine é a mais recente ANTES (ou no
mesmo dia) da compra, isto é, a melhor evidência de como estava o site que a vítima viu.
Usa bisect (busca binária) numa lista ordenada de datas. Também mede as maiores lacunas entre
capturas (períodos em que NÃO temos prova de como o site estava) e grava um CSV.
100% offline: usa caso/dados/.
"""

import bisect                         # busca binária em lista ordenada
import csv
import json
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

MAIORES_LACUNAS = 3  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"

try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO = timezone(timedelta(hours=-3))

# ── Capturas, em ordem, com data local ────────────────────────────────────
cabecalho, *linhas = json.loads((PASTA_CASO / "wayback_cdx_megaoferta.json").read_text(encoding="utf-8"))
capturas = []
for linha in linhas:
    c = dict(zip(cabecalho, linha))
    c["quando"] = datetime.strptime(c["timestamp"], "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc).astimezone(FUSO)
    c["url_arquivo"] = f"https://web.archive.org/web/{c['timestamp']}/{c['original']}"
    capturas.append(c)
capturas.sort(key=lambda c: c["quando"])
datas_capturas = [c["quando"].date() for c in capturas]   # lista ORDENADA: requisito do bisect

# ── Para cada denúncia, a captura mais recente até o dia da compra ────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    denuncias = sorted(csv.DictReader(arquivo, delimiter=";"), key=lambda d: d["data"])

resultado = []
for d in denuncias:
    dia = date.fromisoformat(d["data"])
    # bisect_right devolve a posição onde 'dia' entraria mantendo a ordem, DEPOIS de iguais.
    # Então a posição - 1 é a última captura com data <= dia.
    i = bisect.bisect_right(datas_capturas, dia) - 1
    if i < 0:
        resultado.append({**d, "captura": "", "dias_de_defasagem": "", "length": "", "url_arquivo": ""})
        continue
    c = capturas[i]
    resultado.append({"id": d["id"], "data": d["data"], "produto": d["produto"],
                      "captura": c["timestamp"], "dias_de_defasagem": (dia - datas_capturas[i]).days,
                      "length": c["length"], "url_arquivo": c["url_arquivo"]})

versoes = Counter(r["captura"] for r in resultado)
print("🖼️ Qual versão arquivada cada vítima provavelmente viu:\n")
for c in capturas:
    qtd = versoes.get(c["timestamp"], 0)
    print(f"   {c['quando']:%d/%m/%Y %H:%M}  {c['length']:>5} bytes  HTTP {c['statuscode']}  ← {qtd:>2} denúncias")

pior = max(resultado, key=lambda r: r["dias_de_defasagem"] if r["dias_de_defasagem"] != "" else -1)
print(f"\n⏳ Maior defasagem: {pior['id']} ({pior['data']}) comprou {pior['dias_de_defasagem']} dias "
      f"depois da captura mais próxima. Quanto maior a defasagem, mais fraca a prova.")

# ── Lacunas entre capturas consecutivas ───────────────────────────────────
lacunas = sorted(((b["quando"] - a["quando"], a, b) for a, b in zip(capturas, capturas[1:])),
                 key=lambda x: x[0], reverse=True)
print(f"\n🕳️ As {MAIORES_LACUNAS} maiores lacunas (sem nenhuma captura):")
for delta, a, b in lacunas[:MAIORES_LACUNAS]:
    dentro = sum(1 for d in denuncias if a["quando"].date() < date.fromisoformat(d["data"]) < b["quando"].date())
    print(f"   {a['quando']:%d/%m} → {b['quando']:%d/%m}: {delta.days} dias, {dentro} denúncias no escuro")

SAIDAS.mkdir(exist_ok=True)
with open(SAIDAS / "vitrine_vista_por_denuncia.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=list(resultado[0]), delimiter=";", extrasaction="ignore")
    escritor.writeheader()
    escritor.writerows(resultado)
print("\n💾 saidas/vitrine_vista_por_denuncia.csv gravado.")
print("💡 Próximo passo real: pedir a captura (Save Page Now) das páginas de um golpe ativo ANTES que ele suma.")
