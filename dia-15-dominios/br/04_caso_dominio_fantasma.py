"""
Caso Vitrine Fantasma: o domínio da loja falsa nasceu quando?

Carta 36 (rank A) — Jutsu do Registro Estruturado (aplicação no caso)

O que você aprende:
  • a cruzar a data de criação do domínio (RDAP/WHOIS) com as datas das denúncias;
  • a medir "quantos dias de vida o site tinha quando fez a primeira vítima";
  • a comparar RDAP x WHOIS: as duas fontes concordam?

Este script é 100% offline: usa os dados fictícios de caso/dados/.

Como rodar (dentro da pasta dia-15-dominios):
    python br/04_caso_dominio_fantasma.py
"""

import csv
import json
from datetime import date, datetime
from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"

# ── 1. O que diz o RDAP ───────────────────────────────────────────────────
rdap = json.loads((PASTA_CASO / "rdap_megaoferta.json").read_text(encoding="utf-8"))
eventos = {e["eventAction"]: e["eventDate"] for e in rdap["events"]}
criado_rdap = datetime.fromisoformat(eventos["registration"].replace("Z", "+00:00")).date()

# ── 2. O que diz o WHOIS (formato registro.br: created: AAAAMMDD #id) ─────
criado_whois = None
for linha in (PASTA_CASO / "whois_megaoferta.txt").read_text(encoding="utf-8").splitlines():
    if linha.startswith("created:"):
        aaaammdd = linha.split(":", 1)[1].split()[0]           # "20251002"
        criado_whois = datetime.strptime(aaaammdd, "%Y%m%d").date()

print(f"🌐 Domínio investigado: {rdap['ldhName']}")
print(f"🗓️  Criação segundo o RDAP : {criado_rdap:%d/%m/%Y}")
print(f"🗓️  Criação segundo o WHOIS: {criado_whois:%d/%m/%Y}")
print("✅ As fontes concordam." if criado_rdap == criado_whois else "🚩 As fontes DISCORDAM: anote no relatório!")

# ── 3. A primeira e a última denúncia ─────────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    datas = [date.fromisoformat(linha["data"]) for linha in csv.DictReader(arquivo, delimiter=";")]

primeira, ultima = min(datas), max(datas)
print(f"\n📨 Primeira denúncia: {primeira:%d/%m/%Y}  ·  Última: {ultima:%d/%m/%Y}")
print(f"⏳ O site tinha {(primeira - criado_rdap).days} dias de vida na primeira vítima.")
print(f"⏳ E {(ultima - criado_rdap).days} dias na última.")

# ── 4. Quem aparece como titular? ─────────────────────────────────────────
for entidade in rdap.get("entities", []):
    if "registrant" in entidade.get("roles", []):
        # vCard é uma lista de listas: procuramos o campo "fn" (nome completo)
        nome = next((c[3] for c in entidade["vcardArray"][1] if c[0] == "fn"), "?")
        print(f"\n👤 Titular declarado no registro: {nome} (handle {entidade.get('handle')})")
        print("   Lembre-se: dado de registro pode ser falso ou de laranja. É pista, não prova.")
