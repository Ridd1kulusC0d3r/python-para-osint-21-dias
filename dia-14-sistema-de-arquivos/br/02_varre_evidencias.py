"""
Varrer a sala de evidências: CPFs, chaves PIX e e-mails em todos os arquivos.

Carta 35 (rank A) — Jutsu da Sala de Evidências (parte 2)

O que você aprende:
  • a juntar rglob (Dia 14) com regex (Dia 11) para varrer uma pasta inteira;
  • a pular arquivos que não são texto sem o script quebrar;
  • a montar um relatório "arquivo × tipo de dado" e um índice reverso
    "valor → arquivos onde aparece" (ótimo para achar ligações);
  • a gravar o relatório em CSV para abrir no Excel.

Este script é 100% offline: varre caso/dados (fictício).

Como rodar (dentro da pasta dia-14-sistema-de-arquivos):
    python br/02_varre_evidencias.py
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
# Caminho relativo à pasta do dia (ou absoluto, se preferir).
PASTA_ALVO = "../caso/dados"  #@param {type:"string"}
EXTENSOES = ".txt,.csv,.html,.json,.sql"  #@param {type:"string"}

PADROES = {
    "CPF": re.compile(r"(?<!\d)\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)"),
    "Chave PIX": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "E-mail": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
}

pasta = (PASTA_DIA / PASTA_ALVO).resolve()   # "/" com caminho absoluto usa só o absoluto
extensoes = {e.strip().lower() for e in EXTENSOES.split(",")}

relatorio = []                       # uma linha por arquivo
onde_aparece = defaultdict(set)      # (tipo, valor) → arquivos
pulados = []

# ── 1. Percorrer todos os arquivos, em todas as subpastas ─────────────────
for arquivo in sorted(pasta.rglob("*")):
    if not arquivo.is_file() or arquivo.suffix.lower() not in extensoes:
        continue
    if arquivo.name == "ficha_do_caso.json":
        continue      # é o gabarito do caso: não conta como evidência
    try:
        texto = arquivo.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as erro:
        pulados.append(f"{arquivo.name} ({type(erro).__name__})")
        continue

    nome = str(arquivo.relative_to(pasta))
    linha = {"arquivo": nome}
    for tipo, padrao in PADROES.items():
        achados = set(padrao.findall(texto))          # set: cada valor uma vez por arquivo
        linha[tipo] = len(achados)
        for valor in achados:
            onde_aparece[(tipo, valor.lower())].add(nome)
    relatorio.append(linha)

# ── 2. Tabela arquivo × tipo ──────────────────────────────────────────────
print(f"🗂️  Varredura de {pasta.name}/  ({len(relatorio)} arquivos lidos)\n")
print(f"   {'arquivo':<34} {'CPF':>5} {'PIX':>5} {'E-mail':>7}")
for l in relatorio:
    print(f"   {l['arquivo']:<34} {l['CPF']:>5} {l['Chave PIX']:>5} {l['E-mail']:>7}")
if pulados:
    print(f"\n   ⚠️ Pulados (não são texto UTF-8): {', '.join(pulados)}")

# ── 3. Índice reverso: o que aparece em MAIS arquivos ─────────────────────
print("\n🔗 Valores que ligam vários arquivos (PIX e e-mail em 2+ arquivos):")
for (tipo, valor), arquivos in sorted(onde_aparece.items(), key=lambda par: -len(par[1])):
    if tipo != "CPF" and len(arquivos) >= 2:
        print(f"   {tipo:<9} {valor}  → {len(arquivos)} arquivos")
        print(f"             {', '.join(sorted(arquivos))}")

cpfs = [v for (t, v) in onde_aparece if t == "CPF"]
print(f"\n🔒 {len(cpfs)} CPFs distintos encontrados (dados de vítimas: não listados na tela).")

# ── 4. Salvar ─────────────────────────────────────────────────────────────
saidas = PASTA_DIA / "saidas"
saidas.mkdir(exist_ok=True)
with open(saidas / "varredura_evidencias.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=["arquivo", *PADROES], delimiter=";")
    escritor.writeheader()
    escritor.writerows(relatorio)
print("💾 saidas/varredura_evidencias.csv gravado.")
