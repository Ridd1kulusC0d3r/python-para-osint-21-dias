"""
Teste de fumaça: roda TODOS os exercícios BR e gabaritos e verifica a estrutura de cada dia.

    python ferramentas/smoke_test.py --offline                 # sem internet (sempre deve passar)
    python ferramentas/smoke_test.py                           # ao vivo: descobre APIs que mudaram
    python ferramentas/smoke_test.py --originais               # confere se original/ continua idêntico ao do cipher387
    python ferramentas/smoke_test.py --relatorio relatorio.md  # grava um relatório em Markdown

O que é verificado:
  1. dia.json válido (cartas com número/rank certos, quiz com resposta existente);
  2. todo br/*.py e desafio_gabarito.py roda sem erro (timeout de 120 s);
  3. no modo ao vivo, quem caiu no "⚠️ MODO OFFLINE" é listado como API com problema;
  4. todo original/*.py compila (compile) — eles não rodam aqui porque exigem pip e internet;
  5. com --originais, o código de original/ é comparado linha a linha com o repositório do cipher387.

Só biblioteca padrão. Sai com código 1 se houver falha.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import RAIZ, dias  # noqa: E402

MARCA_OFFLINE = "⚠️ MODO OFFLINE"
URL_CRU = "https://raw.githubusercontent.com/cipher387/python-for-OSINT-21-days/main/Day_{dia}/{arquivo}"


def rank_esperado(dia, nivel):
    if nivel == 3:
        return "S"
    if nivel == 1:
        return "D" if dia <= 10 else "C"
    return "B" if dia <= 10 else "A"


def validar_meta(meta):
    erros = []
    dia = meta.get("dia")
    for chave in ("dia", "slug", "titulo", "capitulo", "cartas", "quiz"):
        if chave not in meta:
            erros.append(f"dia.json sem a chave '{chave}'")
    if meta.get("slug") != meta["_pasta"].name:
        erros.append(f"slug '{meta.get('slug')}' diferente da pasta '{meta['_pasta'].name}'")
    cartas = meta.get("cartas", [])
    if dia and dia > 0:
        if len(cartas) != 3:
            erros.append(f"esperava 3 cartas, achei {len(cartas)}")
        for c in cartas:
            nivel = c.get("nivel")
            if c.get("numero") != dia + 21 * (nivel - 1):
                erros.append(f"carta nível {nivel} deveria ser nº {dia + 21 * (nivel - 1)}, está {c.get('numero')}")
            if c.get("rank") != rank_esperado(dia, nivel):
                erros.append(f"carta {c.get('numero')} deveria ter rank {rank_esperado(dia, nivel)}")
            if len(c.get("efeito", "")) > 160:
                erros.append(f"carta {c.get('numero')}: efeito longo demais ({len(c['efeito'])} caracteres)")
    for i, q in enumerate(meta.get("quiz", []), 1):
        if not 0 <= q.get("correta", -1) < len(q.get("opcoes", [])):
            erros.append(f"quiz {i}: índice 'correta' fora das opções")
    for arquivo in ("README.md", "desafio.md"):
        if not (meta["_pasta"] / arquivo).exists():
            erros.append(f"falta {arquivo}")
    return erros


def rodar(script, pasta, offline):
    ambiente = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    if offline:
        ambiente["OSINT_OFFLINE"] = "1"
    else:
        ambiente.pop("OSINT_OFFLINE", None)
    inicio = time.time()
    try:
        r = subprocess.run([sys.executable, str(script)], cwd=pasta, env=ambiente,
                           capture_output=True, text=True, encoding="utf-8", timeout=120)
        saida = r.stdout + r.stderr
        return r.returncode == 0, saida, time.time() - inicio
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT (120 s)", time.time() - inicio


def codigo_sem_comentarios_novos(texto):
    """Remove o cabeçalho de atribuição e as linhas '# 💬', e normaliza espaços no fim."""
    linhas = texto.splitlines()
    while linhas and (linhas[0].startswith("#") or not linhas[0].strip()):
        linhas.pop(0)
    return [l.rstrip() for l in linhas if l.strip() and not l.lstrip().startswith("# 💬")]


def comparar_original(arquivo, dia):
    url = URL_CRU.format(dia=dia, arquivo=urllib.parse.quote(arquivo.name))
    with urllib.request.urlopen(url, timeout=20) as r:
        upstream = r.read().decode("utf-8", errors="replace")
    nosso = codigo_sem_comentarios_novos(arquivo.read_text(encoding="utf-8"))
    deles = [l.rstrip() for l in upstream.splitlines() if l.strip()]
    return nosso == deles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--originais", action="store_true")
    parser.add_argument("--relatorio")
    parser.add_argument("dias", nargs="*", type=int, help="só estes dias (padrão: todos)")
    args = parser.parse_args()

    falhas, apis, linhas = [], [], []
    modo = "offline" if args.offline else "ao vivo"
    linhas.append(f"# Relatório do teste de fumaça ({modo})\n")
    linhas.append(f"Gerado em {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())} · Python {sys.version.split()[0]}\n")
    linhas.append("| Dia | Arquivo | Resultado | Tempo |\n|---|---|---|---|")

    for meta in dias():
        pasta, dia = meta["_pasta"], meta["dia"]
        if args.dias and dia not in args.dias:
            continue
        for erro in validar_meta(meta):
            falhas.append(f"{pasta.name}: {erro}")
            linhas.append(f"| {dia:02d} | dia.json | ❌ {erro} | |")

        for original in sorted((pasta / "original").glob("*.py")) if (pasta / "original").exists() else []:
            try:
                compile(original.read_text(encoding="utf-8"), str(original), "exec")
            except SyntaxError as erro:
                if original.name.startswith("codigo_com_erro"):
                    continue  # o Dia 21 tem um arquivo com erro de propósito
                falhas.append(f"{pasta.name}/original/{original.name}: não compila ({erro})")
                linhas.append(f"| {dia:02d} | original/{original.name} | ❌ não compila | |")
            if args.originais and not original.name.startswith(("2026_", "nivel1_", "codigo_com_erro")):
                try:
                    igual = comparar_original(original, dia)
                    icone = "✅ idêntico ao upstream" if igual else "❌ DIFERENTE do upstream"
                    if not igual:
                        falhas.append(f"{pasta.name}/original/{original.name}: código difere do cipher387")
                except Exception as erro:
                    icone = f"⚠️ não deu para comparar ({erro})"
                linhas.append(f"| {dia:02d} | original/{original.name} | {icone} | |")

        scripts = sorted((pasta / "br").glob("*.py")) + sorted(pasta.glob("desafio_gabarito.py"))
        for script in scripts:
            ok, saida, tempo = rodar(script, pasta, args.offline)
            nome = script.relative_to(pasta).as_posix()
            if not ok:
                falhas.append(f"{pasta.name}/{nome}: falhou\n{saida[-800:]}")
                resultado = "❌ falhou"
            elif not args.offline and MARCA_OFFLINE in saida:
                apis.append(f"{pasta.name}/{nome}")
                resultado = "🟡 caiu na amostra offline (API mudou ou bloqueou?)"
            else:
                resultado = "✅ ok"
            linhas.append(f"| {dia:02d} | {nome} | {resultado} | {tempo:.1f}s |")
            print(f"{resultado[:2]} {pasta.name}/{nome} ({tempo:.1f}s)")

        # limpeza: o teste não deve deixar lixo
        for lixo in ("saidas",):
            alvo = pasta / lixo
            if alvo.exists() and os.environ.get("MANTER_SAIDAS") != "1":
                for arq in sorted(alvo.rglob("*"), reverse=True):
                    arq.unlink() if arq.is_file() else arq.rmdir()
                alvo.rmdir()

    linhas.append(f"\n**Falhas:** {len(falhas)} · **APIs com problema:** {len(apis)}\n")
    if apis:
        linhas.append("## 🟡 Exercícios que caíram na amostra offline\n")
        linhas += [f"- `{a}`" for a in apis]
    if falhas:
        linhas.append("\n## ❌ Falhas\n")
        linhas += [f"```\n{f}\n```" for f in falhas]

    relatorio = "\n".join(linhas)
    if args.relatorio:
        Path(args.relatorio).write_text(relatorio, encoding="utf-8")
    print(f"\nFalhas: {len(falhas)} · APIs com problema: {len(apis)}")
    for f in falhas:
        print("❌", f)
        if os.environ.get("GITHUB_ACTIONS"):
            # Anotação visível na aba "Checks" do GitHub (sem precisar baixar o log)
            resumo = f.replace("%", "%25").replace("\r", "").replace("\n", "%0A")[-1800:]
            print(f"::error title=smoke_test::{resumo}")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
