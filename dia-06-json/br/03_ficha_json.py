"""
Montar a ficha de evidências do caso em JSON, salvar, reler e conferir.

Carta 27 (rank B) — Jutsu do Mapa do JSON (parte 3)

O que você aprende:
  • a montar um dicionário com listas e dicionários dentro (estrutura aninhada);
  • json.dump(..., indent=2, ensure_ascii=False): JSON legível e com acentos de verdade;
  • a reler o arquivo com json.load e conferir que nada se perdeu ("ida e volta");
  • o que o JSON NÃO guarda direto (datas, Decimal, conjuntos) e como contornar.

Como rodar (dentro da pasta dia-06-json):
    python br/03_ficha_json.py
"""

import csv
import json
import re
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"

try:
    from zoneinfo import ZoneInfo
    FUSO_BR = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO_BR = timezone(timedelta(hours=-3))

# ── 1. Juntar o que já sabemos (dias 4, 5 e 6) ────────────────────────────
html = (PASTA_CASO / "vitrine_megaoferta.html").read_text(encoding="utf-8")
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    denuncias = list(csv.DictReader(arquivo, delimiter=";"))

# Conjunto (set) de chaves PIX: tira repetidas. JSON não conhece set → viramos lista ordenada.
chaves_pix = sorted({d["chave_pix_destino"] for d in denuncias})
# Dinheiro: Decimal soma sem erro de centavo. JSON não conhece Decimal → guardamos como texto.
total = sum(Decimal(d["valor"]) for d in denuncias)
# Datas: JSON não conhece date → usamos texto no formato ISO (AAAA-MM-DD).
datas = [date.fromisoformat(d["data"]) for d in denuncias]

ficha = {
    "caso": "Operação Vitrine Fantasma",
    "gerado_em": datetime.now(FUSO_BR).isoformat(timespec="seconds"),
    "loja": {
        "nome": "MegaOferta Brasil",
        "dominio": "megaoferta-brasil.example",
        "cnpj_rodape": re.search(r"CNPJ\s*([\d./-]+)", html).group(1),
        "cnpj_valido": False,                          # conclusão do script 02
        "cep_rodape": re.search(r"CEP\s*(\d{5}-?\d{3})", html).group(1),
        "cep_corresponde_a": "Praça Sete de Setembro, Centro, Belo Horizonte/MG",  # Dia 5
    },
    "denuncias": {
        "quantidade": len(denuncias),
        "primeira": min(datas).isoformat(),
        "ultima": max(datas).isoformat(),
        "valor_total": str(total),                     # "54877.40": texto, sem perder centavos
    },
    "chaves_pix": chaves_pix,
    "evidencias": [
        {"id": "EV-01", "descricao": "Cópia da vitrine", "arquivo": "caso/dados/vitrine_megaoferta.html"},
        {"id": "EV-02", "descricao": "Planilha de denúncias", "arquivo": "caso/dados/denuncias.csv"},
    ],
}

# ── 2. Salvar ─────────────────────────────────────────────────────────────
SAIDAS.mkdir(exist_ok=True)
caminho = SAIDAS / "ficha_evidencias.json"
with open(caminho, "w", encoding="utf-8") as arquivo:
    # indent=2 → uma informação por linha, com recuo (fácil de ler e de comparar no git)
    # ensure_ascii=False → grava "Praça" em vez de "Praça"
    json.dump(ficha, arquivo, indent=2, ensure_ascii=False)
print(f"💾 Ficha salva em {caminho.relative_to(PASTA_DIA)} ({caminho.stat().st_size} bytes)")

# ── 3. Reler e conferir a "ida e volta" ───────────────────────────────────
with open(caminho, encoding="utf-8") as arquivo:
    relida = json.load(arquivo)
print("✅ Releitura idêntica ao original." if relida == ficha else "🚩 Algo mudou na releitura!")

# ── 4. Navegar na ficha relida ────────────────────────────────────────────
print(f"\n🏢 {relida['loja']['nome']} · CNPJ {relida['loja']['cnpj_rodape']} "
      f"({'válido' if relida['loja']['cnpj_valido'] else 'INVÁLIDO'})")
print(f"📨 {relida['denuncias']['quantidade']} denúncias de {relida['denuncias']['primeira']} "
      f"a {relida['denuncias']['ultima']}")
print(f"💰 Total: R$ {Decimal(relida['denuncias']['valor_total'])}  ← de volta a Decimal para fazer conta")
print(f"🔑 {len(relida['chaves_pix'])} chaves PIX distintas:")
for chave in relida["chaves_pix"]:
    print(f"   • {chave}")

# ── 5. O que acontece se tentarmos salvar um tipo que o JSON não conhece? ─
try:
    json.dumps({"data": date(2025, 10, 12)})
except TypeError as erro:
    print(f"\n💡 Lição: {erro}. Por isso convertemos datas para texto ISO antes de salvar.")
