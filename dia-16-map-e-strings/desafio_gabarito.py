"""
Gabarito do Desafio S do Dia 16 — Detector de grafias compatíveis.

Decide se duas formas de um nome podem ser a MESMA pessoa, aceitando acentos,
maiúsculas, pontuação e iniciais abreviadas ("Kaua T Brandao" ≈ "Kauã Teixeira Brandão").
Depois agrupa todas as grafias encontradas nas evidências do caso.
100% offline: usa só caso/dados/.
"""

import csv
import itertools
import json
import unicodedata
from pathlib import Path

NOME_ALVO = "Kauã Teixeira Brandão"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
PARTICULAS = {"da", "de", "do", "das", "dos", "e"}


def tokens(nome):
    """'Kauã T. Brandão' → ['kaua', 't', 'brandao'] (sem acento, sem pontuação, sem partículas)."""
    sem = "".join(c for c in unicodedata.normalize("NFKD", nome) if not unicodedata.combining(c))
    limpo = "".join(c if c.isalnum() else " " for c in sem.casefold())
    return [t for t in limpo.split() if t not in PARTICULAS]


def pedaco_compativel(a, b):
    """Dois pedaços combinam se são iguais ou se um é a inicial do outro."""
    if a == b:
        return True
    if len(a) == 1 or len(b) == 1:
        return a[0] == b[0]
    return False


def compativel(nome1, nome2):
    """Mesmo número de partes, primeiro e último nome iguais por extenso, meio compatível.

    Exigir o sobrenome por extenso evita juntar "K. Brandão" com "Kátia Brandão" por acaso.
    """
    t1, t2 = tokens(nome1), tokens(nome2)
    if len(t1) != len(t2) or len(t1) < 2:
        return False
    if t1[-1] != t2[-1]:                       # sobrenome final precisa ser idêntico
        return False
    return all(pedaco_compativel(a, b) for a, b in zip(t1, t2))


# ── Testes rápidos (assert para se a regra quebrar) ───────────────────────
assert compativel("Kaua T Brandao", "Kauã Teixeira Brandão")
assert compativel("KAUÃ T. BRANDÃO", "kaua teixeira brandao")
assert not compativel("Kauã Brandão", "Kauã Teixeira Brandão")       # número de partes diferente
assert not compativel("M. R. Brandão", "Kauã Teixeira Brandão")
assert compativel("Maria da Silva", "MARIA SILVA")                    # partícula ignorada

# ── Coletar grafias de nomes nas evidências ───────────────────────────────
grafias = {}   # nome → de onde veio

rdap = json.loads((PASTA_CASO / "rdap_megaoferta.json").read_text(encoding="utf-8"))
for ent in rdap.get("entities", []):
    for campo in ent["vcardArray"][1]:
        if campo[0] == "fn":
            grafias[campo[3]] = "RDAP"

for linha in (PASTA_CASO / "whois_megaoferta.txt").read_text(encoding="utf-8").splitlines():
    if linha.startswith("owner:"):
        grafias.setdefault(linha.split(":", 1)[1].strip(), "WHOIS")

with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    for linha in csv.DictReader(arquivo, delimiter=";"):
        grafias.setdefault(linha["nome_vitima"], "denúncia")

grafias.setdefault(NOME_ALVO, "parâmetro")

# ── Agrupar: cada grupo junta grafias compatíveis entre si ────────────────
grupos = []
for nome in grafias:
    for grupo in grupos:
        if any(compativel(nome, outro) for outro in grupo):
            grupo.append(nome)
            break
    else:                                       # for...else: roda se não houve break
        grupos.append([nome])

print("(RDAP e WHOIS trazem a MESMA grafia, por isso ela aparece uma vez só.)")
print(f"🧾 {len(grafias)} grafias coletadas → {len(grupos)} pessoas prováveis\n")
for grupo in grupos:
    if len(grupo) > 1:
        print("🔗 Grupo com mais de uma grafia:")
        for nome in grupo:
            print(f"   • {nome:<28} ({grafias[nome]})")

alvo_grupo = next(g for g in grupos if NOME_ALVO in g)
print(f"\n🎯 Grafias compatíveis com {NOME_ALVO}: {len(alvo_grupo)}")

# Pares "quase iguais" que NÃO foram juntados (bom para revisão humana):
# mesmo primeiro nome E mesmo último sobrenome, mas a regra disse "não".
quase = [(a, b) for a, b in itertools.combinations(grafias, 2)
         if tokens(a)[0] == tokens(b)[0] and tokens(a)[-1] == tokens(b)[-1] and not compativel(a, b)]
print(f"🤔 Mesmo primeiro e último nome, mas NÃO compatíveis (revisar à mão): {len(quase)}")
for a, b in quase[:5]:
    print(f"   {a}  ×  {b}")
