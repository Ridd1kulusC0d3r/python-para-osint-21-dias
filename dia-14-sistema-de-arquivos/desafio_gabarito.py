"""
Gabarito do Desafio S do Dia 14 — Triagem do pendrive apreendido.

Varre dados/pendrive_apreendido/ (fictício) e, para cada arquivo:
  • calcula o SHA-256 em blocos;
  • descobre o tipo REAL pelos primeiros bytes ("número mágico") e compara com a extensão;
  • marca duplicatas (mesmo hash, nomes diferentes);
  • marca o que já é conhecido (hash igual a algum arquivo de caso/dados).
Grava saidas/triagem_pendrive.csv. 100% offline.
"""

import csv
import hashlib
from collections import defaultdict
from pathlib import Path

PASTA_PENDRIVE = "dados/pendrive_apreendido"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"

# Assinaturas de início de arquivo ("magic numbers") mais comuns.
MAGICOS = [
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"\xff\xd8\xff", "jpg"),
    (b"%PDF-", "pdf"),
    (b"PK\x03\x04", "zip"),            # também é o começo de .docx, .xlsx, .apk…
    (b"GIF8", "gif"),
    (b"SQLite format 3\x00", "sqlite"),
]
# Extensões que aceitamos como "compatíveis" com cada tipo real.
COMPATIVEIS = {
    "png": {".png"}, "jpg": {".jpg", ".jpeg"}, "pdf": {".pdf"}, "gif": {".gif"},
    "zip": {".zip", ".docx", ".xlsx", ".pptx", ".odt", ".apk", ".jar"},
    "sqlite": {".db", ".sqlite", ".sqlite3"},
    "texto": {".txt", ".csv", ".html", ".htm", ".json", ".sql", ".md", ".xml"},
}


def sha256(caminho, bloco=65536):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for pedaco in iter(lambda: f.read(bloco), b""):   # lê até devolver b"" (fim)
            h.update(pedaco)
    return h.hexdigest()


def tipo_real(caminho):
    with open(caminho, "rb") as f:
        inicio = f.read(16)
    for assinatura, tipo in MAGICOS:
        if inicio.startswith(assinatura):
            return tipo
    try:
        inicio.decode("utf-8")       # não é binário conhecido; se decodifica, tratamos como texto
        return "texto"
    except UnicodeDecodeError:
        return "desconhecido"


# ── 1. Hashes já conhecidos (as evidências que o NFA já tem) ──────────────
conhecidos = {sha256(p): p.relative_to(PASTA_CASO).as_posix() for p in PASTA_CASO.rglob("*") if p.is_file()}

# ── 2. Varredura do pendrive ──────────────────────────────────────────────
pendrive = PASTA_DIA / PASTA_PENDRIVE
linhas, por_hash = [], defaultdict(list)
for arquivo in sorted(p for p in pendrive.rglob("*") if p.is_file()):
    try:
        h, tipo = sha256(arquivo), tipo_real(arquivo)
    except OSError as erro:
        print(f"⚠️  Não consegui ler {arquivo.name}: {erro}")
        continue
    nome = arquivo.relative_to(pendrive).as_posix()
    extensao_ok = arquivo.suffix.lower() in COMPATIVEIS.get(tipo, set())
    linhas.append({"arquivo": nome, "bytes": arquivo.stat().st_size, "tipo_real": tipo,
                   "extensao_ok": "sim" if extensao_ok else "NÃO", "sha256": h,
                   "ja_conhecido": conhecidos.get(h, ""), "duplicata_de": ""})
    por_hash[h].append(nome)

# ── 3. Marcar duplicatas (o primeiro nome em ordem alfabética é o "original") ─
for linha in linhas:
    irmaos = por_hash[linha["sha256"]]
    if len(irmaos) > 1 and linha["arquivo"] != irmaos[0]:
        linha["duplicata_de"] = irmaos[0]

# ── 4. Relatório ──────────────────────────────────────────────────────────
print(f"🔌 Triagem de {PASTA_PENDRIVE}/ ({len(linhas)} arquivos)\n")
for l in linhas:
    alertas = []
    if l["extensao_ok"] == "NÃO":
        alertas.append(f"🎭 extensão mente: é {l['tipo_real'].upper()}")
    if l["duplicata_de"]:
        alertas.append(f"♊ cópia de {l['duplicata_de']}")
    if l["ja_conhecido"]:
        alertas.append(f"📁 já temos: {l['ja_conhecido']}")
    print(f"   {l['sha256'][:12]}…  {l['arquivo']:<28} {' · '.join(alertas) or '🆕 novo'}")

novos = [l for l in linhas if not l["ja_conhecido"] and not l["duplicata_de"]]
print(f"\n📊 {len(linhas)} arquivos · {len(novos)} realmente novos para analisar · "
      f"{sum(l['extensao_ok'] == 'NÃO' for l in linhas)} com extensão falsa")

saidas = PASTA_DIA / "saidas"
saidas.mkdir(exist_ok=True)
with open(saidas / "triagem_pendrive.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=list(linhas[0]), delimiter=";")
    escritor.writeheader()
    escritor.writerows(linhas)
print("💾 saidas/triagem_pendrive.csv gravado.")
