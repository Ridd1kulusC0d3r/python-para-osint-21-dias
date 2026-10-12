"""
Gabarito do Desafio S do Dia 13 — Fila de diligências por chave PIX.

Para cada chave PIX do caso, monta a lista de vítimas em ordem de data, calcula
total (Decimal), primeira e última denúncia, a cidade mais frequente e as cidades
em ordem alfabética correta (com acento). Depois ordena as chaves pelo valor total:
a de maior prejuízo vira a primeira diligência. Grava saidas/fila_diligencias.txt.
100% offline: só caso/dados (fictício).
"""

import csv
import unicodedata
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"

OFICIAIS = ["Belo Horizonte", "Betim", "Contagem", "Divinópolis", "Governador Valadares",
            "Ipatinga", "Juiz de Fora", "Poços de Caldas", "Sete Lagoas", "Uberaba", "Uberlândia"]


def sem_acento(texto):
    separado = unicodedata.normalize("NFKD", texto.strip())
    return "".join(c for c in separado if not unicodedata.combining(c)).casefold()


OFICIAL = {sem_acento(n): n for n in OFICIAIS}
OFICIAL["belo horizone"] = "Belo Horizonte"     # erro de digitação conhecido


def brl(valor):
    """Decimal('1999.9') → 'R$ 1.999,90' (troca de separadores via um caractere temporário)."""
    return "R$ " + f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


# ── 1. Agrupar as denúncias por chave ─────────────────────────────────────
por_chave = defaultdict(list)                  # chave → lista de denúncias (dicionários)
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as f:
    for linha in csv.DictReader(f, delimiter=";"):
        linha["cidade"] = OFICIAL.get(sem_acento(linha["cidade"]), linha["cidade"])
        linha["valor"] = Decimal(linha["valor"])
        por_chave[linha["chave_pix_destino"]].append(linha)

# ── 2. Resumo de cada chave ───────────────────────────────────────────────
fila = []
for chave, lista in por_chave.items():
    lista.sort(key=lambda d: (d["data"], d["id"]))   # data ISO ordena certo como texto
    cidades = [d["cidade"] for d in lista]
    fila.append({
        "chave": chave,
        "vitimas": len(lista),
        "total": sum((d["valor"] for d in lista), Decimal("0")),
        "primeira": lista[0]["data"],                 # [0] = primeiro da lista ordenada
        "ultima": lista[-1]["data"],                  # [-1] = último
        "cidade_top": Counter(cidades).most_common(1)[0],
        "cidades": sorted(set(cidades), key=lambda c: (sem_acento(c), c)),
        "ids": [d["id"] for d in lista],
    })

# ── 3. Ordenar a fila: maior prejuízo primeiro (desempate: mais vítimas) ──
fila.sort(key=lambda item: (item["total"], item["vitimas"]), reverse=True)

linhas_relatorio = ["FILA DE DILIGÊNCIAS POR CHAVE PIX (maior prejuízo primeiro)", ""]
for posicao, item in enumerate(fila, start=1):
    bloco = [
        f"{posicao}ª diligência · chave {item['chave']}",
        f"   {item['vitimas']} vítimas · {brl(item['total'])} · de {item['primeira']} a {item['ultima']}",
        f"   cidade com mais vítimas: {item['cidade_top'][0]} ({item['cidade_top'][1]})",
        f"   cidades: {', '.join(item['cidades'])}",
        f"   denúncias: {', '.join(item['ids'][:6])}{' …' if len(item['ids']) > 6 else ''}",
        "",
    ]
    linhas_relatorio += bloco
total_geral = sum((i["total"] for i in fila), Decimal("0"))
linhas_relatorio.append(f"TOTAL GERAL: {brl(total_geral)} em {sum(i['vitimas'] for i in fila)} denúncias")

print("\n".join(linhas_relatorio))
saidas = PASTA_DIA / "saidas"
saidas.mkdir(exist_ok=True)
(saidas / "fila_diligencias.txt").write_text("\n".join(linhas_relatorio) + "\n", encoding="utf-8")
print("\n💾 saidas/fila_diligencias.txt gravado.")
