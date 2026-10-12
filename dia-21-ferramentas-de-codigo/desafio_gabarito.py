"""
Gabarito do Desafio S do Dia 21 — O revisor automático do curso.

Lê (SEM executar) todos os br/*.py do repositório com o módulo ast e confere as regras do
CONTRIBUTING.md:
  1. a sintaxe está ok;
  2. tem docstring no topo, com a palavra "Carta" (menos no Dia 0, que não tem cartas);
  3. não usa input();
  4. só importa biblioteca padrão (imports dentro de try/except ImportError contam como opcionais);
  5. todo open()/read_text()/write_text() em modo TEXTO informa encoding= (armadilha do Windows).
Grava saidas/revisao_codigo.csv e imprime um placar por dia.
"""

import ast
import csv
import sys
from collections import defaultdict
from pathlib import Path

SO_PROBLEMAS = False  #@param {type:"boolean"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
RAIZ = PASTA_DIA.parent
SAIDAS = PASTA_DIA / "saidas"

# sys.stdlib_module_names existe a partir do Python 3.10. No 3.9, usamos uma lista mínima.
STDLIB = set(getattr(sys, "stdlib_module_names", ())) or {
    "argparse", "ast", "bisect", "calendar", "collections", "csv", "datetime", "decimal", "difflib",
    "doctest", "glob", "hashlib", "html", "http", "itertools", "json", "locale", "math", "os", "pathlib",
    "platform", "py_compile", "random", "re", "shutil", "socket", "sqlite3", "string", "subprocess",
    "sys", "tempfile", "threading", "time", "unicodedata", "unittest", "urllib", "uuid", "zoneinfo",
}


def imports_opcionais(arvore):
    """Nomes importados dentro de um bloco try cujo except trata ImportError (ou Exception)."""
    opcionais = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Try):
            tratados = {getattr(h.type, "id", None) for h in no.handlers}
            if tratados & {"ImportError", "ModuleNotFoundError", "Exception", None}:
                for filho in no.body:
                    for sub in ast.walk(filho):
                        if isinstance(sub, ast.Import):
                            opcionais |= {a.name.split(".")[0] for a in sub.names}
                        elif isinstance(sub, ast.ImportFrom) and sub.module:
                            opcionais.add(sub.module.split(".")[0])
    return opcionais


def modo_do_open(chamada):
    """Devolve o modo de um open(...) se for um texto fixo; senão, 'r' (o padrão)."""
    if len(chamada.args) >= 2 and isinstance(chamada.args[1], ast.Constant):
        return str(chamada.args[1].value)
    for kw in chamada.keywords:
        if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
            return str(kw.value.value)
    return "r"


def revisar(caminho):
    problemas = []
    sem_cartas = caminho.parts[-3].startswith("dia-00")     # o Dia 0 não tem cartas
    codigo = caminho.read_text(encoding="utf-8")
    try:
        arvore = ast.parse(codigo, filename=str(caminho))
    except SyntaxError as erro:
        return [f"sintaxe: linha {erro.lineno}: {erro.msg}"]

    doc = ast.get_docstring(arvore)
    if not doc:
        problemas.append("sem docstring no topo")
    elif "Carta" not in doc and not sem_cartas:
        problemas.append("docstring sem a linha 'Carta'")

    opcionais = imports_opcionais(arvore)
    for no in ast.walk(arvore):
        # 3. input()
        if isinstance(no, ast.Call) and isinstance(no.func, ast.Name) and no.func.id == "input":
            problemas.append(f"linha {no.lineno}: usa input()")
        # 4. imports fora da stdlib
        nomes = []
        if isinstance(no, ast.Import):
            nomes = [a.name.split(".")[0] for a in no.names]
        elif isinstance(no, ast.ImportFrom) and no.module and no.level == 0:
            nomes = [no.module.split(".")[0]]
        for nome in nomes:
            if nome not in STDLIB and nome not in opcionais:
                problemas.append(f"linha {no.lineno}: importa '{nome}' (não é stdlib)")
        # 5. encoding
        if isinstance(no, ast.Call):
            tem_encoding = any(kw.arg == "encoding" for kw in no.keywords)
            if isinstance(no.func, ast.Name) and no.func.id == "open":
                if "b" not in modo_do_open(no) and not tem_encoding:
                    problemas.append(f"linha {no.lineno}: open() em modo texto sem encoding=")
            elif isinstance(no.func, ast.Attribute) and no.func.attr in ("read_text", "write_text"):
                if not tem_encoding:
                    problemas.append(f"linha {no.lineno}: {no.func.attr}() sem encoding=")
    return problemas


# ── Varrer o repositório ──────────────────────────────────────────────────
linhas = []
placar = defaultdict(lambda: [0, 0])                 # dia → [arquivos, arquivos com problema]
for arquivo in sorted(RAIZ.glob("dia-*/br/*.py")):
    dia = arquivo.parts[-3]
    problemas = revisar(arquivo)
    placar[dia][0] += 1
    placar[dia][1] += bool(problemas)
    linhas.append({"dia": dia, "arquivo": arquivo.name, "ok": "sim" if not problemas else "não",
                   "problemas": " | ".join(problemas)})
    if problemas or not SO_PROBLEMAS:
        print(f"{'✅' if not problemas else '⚠️ '} {dia}/br/{arquivo.name}")
        for p in problemas:
            print(f"      • {p}")

print("\n📋 Placar por dia (arquivos · com apontamento):")
for dia, (total, ruins) in sorted(placar.items()):
    print(f"   {dia:<40} {total:>2} · {ruins}")
total = sum(v[0] for v in placar.values())
ruins = sum(v[1] for v in placar.values())
print(f"\n🧮 {total} scripts revisados, {ruins} com apontamentos. Nada foi executado: só lido com ast.")

SAIDAS.mkdir(exist_ok=True)
with open(SAIDAS / "revisao_codigo.csv", "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=["dia", "arquivo", "ok", "problemas"], delimiter=";")
    escritor.writeheader()
    escritor.writerows(linhas)
print("💾 saidas/revisao_codigo.csv gravado.")
