"""
Gabarito do Desafio S do Dia 11 — Telefones normalizados e cruzados entre fontes.

Procura telefones em TODAS as fontes de texto do caso (conversa, vitrine, depoimentos
e a coluna telefone_contato das denúncias), normaliza cada um para o formato
+55DDNNNNNNNNN e mostra quais números aparecem em mais de uma fonte.
100% offline: só caso/dados (fictício).
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

MIN_FONTES = 2  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"

RE_TEL = re.compile(r"(?<![\d-])(?:\+?55[\s-]?)?\(?[1-9]\d\)?[\s-]?(?:9[\s-]?)?\d{4}[\s-]?\d{4}(?![\d-])")
RE_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
RE_CPF = re.compile(r"\d{3}\.\d{3}\.\d{3}-\d{2}")


def normalizar(bruto):
    """'(31) 98888-0101', '+55 31 9 8888-0101', '5531988880101' → '+5531988880101'."""
    digitos = re.sub(r"\D", "", bruto)
    if len(digitos) in (12, 13) and digitos.startswith("55"):
        digitos = digitos[2:]                     # tira o código do país
    if len(digitos) not in (10, 11):
        return None                               # não parece telefone brasileiro
    return "+55" + digitos


def telefones_no_texto(texto):
    # Apaga UUIDs e CPFs antes, para seus dígitos não virarem "telefones".
    texto = RE_CPF.sub(" ", RE_UUID.sub(" ", texto))
    return [t for t in (normalizar(m) for m in RE_TEL.findall(texto)) if t]


fontes = defaultdict(set)         # telefone → conjunto de fontes onde apareceu

# 1) Arquivos de texto do caso
arquivos = [PASTA_CASO / "conversa_whatsapp.txt", PASTA_CASO / "vitrine_megaoferta.html"]
arquivos += sorted((PASTA_CASO / "depoimentos").glob("*.txt"))
for arquivo in arquivos:
    try:
        texto = arquivo.read_text(encoding="utf-8")
    except OSError as erro:
        print(f"⚠️  Pulei {arquivo.name}: {erro}")
        continue
    # A vitrine também tem o número "colado" no link wa.me/5531988880101
    texto = re.sub(r"wa\.me/(\d+)", r" +\1 ", texto)
    for tel in telefones_no_texto(texto):
        fontes[tel].add(arquivo.name)

# 2) Coluna da planilha de denúncias
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as f:
    for linha in csv.DictReader(f, delimiter=";"):
        tel = normalizar(linha["telefone_contato"])
        if tel:
            fontes[tel].add(f"denuncias.csv ({linha['id']})")

print(f"📞 Telefones distintos encontrados: {len(fontes)}\n")
cruzados = {t: f for t, f in fontes.items() if len(f) >= MIN_FONTES}
print(f"🔗 Aparecem em {MIN_FONTES}+ fontes: {len(cruzados)}")
for tel, onde in sorted(cruzados.items(), key=lambda par: -len(par[1])):
    print(f"   {tel}  ← {len(onde)} fontes: {', '.join(sorted(onde))}")

print("\n🧠 O número do vendedor aparece na vitrine, na conversa e nos depoimentos:")
print("   é o elo que liga o site, o atendimento e as vítimas.")
