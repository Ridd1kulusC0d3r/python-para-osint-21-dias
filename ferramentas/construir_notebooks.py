"""
Gera o notebook.ipynb (Google Colab / Jupyter) de cada dia a partir dos arquivos da pasta.

O notebook nunca é editado à mão: edite README.md, dia.json, original/, br/ e desafio*,
e rode:
    python ferramentas/construir_notebooks.py           # todos os dias
    python ferramentas/construir_notebooks.py 15        # só o dia 15

Só biblioteca padrão.
"""

import json
import re
import sys

import sys as _sys
for _f in (_sys.stdout, _sys.stderr):
    if hasattr(_f, "reconfigure"):
        _f.reconfigure(encoding="utf-8", errors="replace")

from comum import (URL_ORIGINAL, URL_REPO, REPO_GITHUB, dias, entre_marcadores,
                   secao, secoes_markdown, titulo_do_script)


def md(texto):
    return {"cell_type": "markdown", "metadata": {}, "source": texto.strip("\n").splitlines(True)}


def codigo(texto, escondido=False):
    meta = {"cellView": "form"} if escondido else {}
    return {"cell_type": "code", "metadata": meta, "execution_count": None, "outputs": [],
            "source": texto.strip("\n").splitlines(True)}


def corrigir_links(texto, slug):
    """Links relativos do README (ex.: br/x.py) viram links absolutos no GitHub."""
    base = f"{URL_REPO}/blob/main/{slug}/"

    def troca(m):
        alvo = m.group(1)
        if re.match(r"^(https?:|mailto:|#)", alvo):
            return m.group(0)
        if alvo.startswith("../"):
            return f"]({URL_REPO}/blob/main/{alvo[3:]})"
        return f"]({base}{alvo})"

    return re.sub(r"\]\(([^)\s]+)\)", troca, texto)


def limpar_param(texto):
    """Texto seguro para dentro de um #@param (sem aspas que quebrem o formulário)."""
    return texto.replace('"', "'").replace("\n", " ").strip()


def celula_preparo(slug):
    return codigo(f'''
#@title ⚙️ Preparar o ambiente (rode esta célula primeiro)
# No Colab: baixa o repositório e entra na pasta do dia.
# No Jupyter local: o notebook já está na pasta do dia, então não faz nada.
import os, subprocess, sys
from pathlib import Path

REPO = "{URL_REPO}"
if "google.colab" in sys.modules:
    destino = "/content/python-para-osint-21-dias"
    if not os.path.isdir(destino):
        subprocess.run(["git", "clone", "--depth", "1", REPO, destino], check=True)
    os.chdir(f"{{destino}}/{slug}")

PASTA_NB = str(Path.cwd())          # usada pelas células para voltar sempre à pasta certa
print("📂 Pasta do dia:", PASTA_NB)
print("🐍 Python", sys.version.split()[0])
''', escondido=True)


def celula_script(caminho, pasta_rel):
    texto = caminho.read_text(encoding="utf-8")
    # A primeira linha garante que o script rode na pasta certa (original/ ou a pasta do dia),
    # exatamente como rodaria no terminal.
    alvo = "{PASTA_NB}/original" if pasta_rel == "original" else "{PASTA_NB}"
    return codigo(f"%cd -q {alvo}\n" + texto)


def construir(meta):
    pasta = meta["_pasta"]
    slug = pasta.name
    readme = (pasta / "README.md").read_text(encoding="utf-8")
    secoes = secoes_markdown(readme)
    numero = meta["dia"]
    celulas = []

    # ── Abertura ──────────────────────────────────────────────────────────
    cartas = " · ".join(str(c["numero"]) for c in meta.get("cartas", [])) or "—"
    historia = entre_marcadores(readme, "historia")
    celulas.append(md(f"""
# Dia {numero:02d} — {meta['titulo']}

**🃏 Cartas:** {cartas} &nbsp;·&nbsp; **📘 Original:** *{meta.get('titulo_original', '—')}*
&nbsp;·&nbsp; [repositório]({URL_REPO}) &nbsp;·&nbsp; [curso original do cipher387]({URL_ORIGINAL})

---

## 📖 Capítulo {numero} — {meta.get('capitulo', '')}

{corrigir_links(historia, slug)}
"""))
    celulas.append(celula_preparo(slug))

    # ── Objetivos e conceito ──────────────────────────────────────────────
    _, objetivos = secao(secoes, "🎯")
    conceito = entre_marcadores(readme, "conceito")
    celulas.append(md(f"## 🎯 Objetivos\n\n{corrigir_links(objetivos, slug)}\n\n"
                      f"## 🧠 Conceito em 2 minutos\n\n{corrigir_links(conceito, slug)}"))

    # ── Nível 1: original ─────────────────────────────────────────────────
    originais = sorted((pasta / "original").glob("*.py")) if (pasta / "original").exists() else []
    _, texto_n1 = secao(secoes, "🥋")
    celulas.append(md(f"## 🥋 Nível 1 — Exercício original (cipher387)\n\n{corrigir_links(texto_n1, slug)}"))
    if meta.get("pip_original"):
        libs = " ".join(meta["pip_original"])
        celulas.append(codigo(f"#@title 📦 Instalar as bibliotecas do exercício original\n%pip install -q {libs}"))
    for arq in originais:
        celulas.append(md(f"### `original/{arq.name}` — {titulo_do_script(arq)}"))
        celulas.append(celula_script(arq, "original"))

    # ── Nível 2: Brasil ───────────────────────────────────────────────────
    _, texto_n2 = secao(secoes, "🇧🇷")
    celulas.append(md(f"## 🇧🇷 Nível 2 — Camada Brasil\n\n{corrigir_links(texto_n2, slug)}\n\n"
                      "> 💡 Os campos com formulário à direita (`#@param`) podem ser editados sem mexer no código. "
                      "Para testar sem internet, rode antes: `os.environ['OSINT_OFFLINE'] = '1'`."))
    for arq in sorted((pasta / "br").glob("*.py")):
        celulas.append(md(f"### `br/{arq.name}` — {titulo_do_script(arq)}"))
        celulas.append(celula_script(arq, "br"))
    for arq in sorted((pasta / "br").glob("*.md")):
        celulas.append(md(corrigir_links(arq.read_text(encoding="utf-8"), slug)))

    # ── Ética ─────────────────────────────────────────────────────────────
    _, etica = secao(secoes, "⚖️")
    if etica:
        celulas.append(md(f"## ⚖️ Ética, LGPD e OPSEC\n\n{corrigir_links(etica, slug)}"))

    # ── Quiz ──────────────────────────────────────────────────────────────
    if meta.get("quiz"):
        celulas.append(md("## 🎯 Quiz rápido\n\nEscolha a resposta no formulário de cada célula e rode a célula."))
        for i, q in enumerate(meta["quiz"], 1):
            letras = "ABCDEFG"
            opcoes = [f"{letras[j]}) {limpar_param(o)}" for j, o in enumerate(q["opcoes"])]
            lista = json.dumps(["Escolha uma opção"] + opcoes, ensure_ascii=False)
            celulas.append(codigo(f'''
#@title {i}. {limpar_param(q["pergunta"])}
resposta = "Escolha uma opção" #@param {lista}
correta = {json.dumps(opcoes[q["correta"]], ensure_ascii=False)}
if resposta == "Escolha uma opção":
    print("👆 Escolha uma opção no formulário e rode de novo.")
elif resposta == correta:
    print("✅ Acertou!", {json.dumps(q.get("explicacao", ""), ensure_ascii=False)})
else:
    print("❌ Ainda não. Releia o conceito do dia e tente outra vez.")
''', escondido=True))

    # ── Nível 3: desafio ──────────────────────────────────────────────────
    desafio_md = pasta / "desafio.md"
    if desafio_md.exists():
        enunciado = re.sub(r"<details>.*?</details>", "", desafio_md.read_text(encoding="utf-8"), flags=re.S)
        celulas.append(md(corrigir_links(enunciado, slug)))
        celulas.append(codigo("%cd -q {PASTA_NB}\n# ✍️ Escreva sua solução aqui.\n"))
        gabarito = pasta / "desafio_gabarito.py"
        if gabarito.exists():
            celulas.append(codigo('#@title 🔒 Gabarito (dê dois cliques aqui para ver o código) { display-mode: "form" }\n'
                                  "%cd -q {PASTA_NB}\n" + gabarito.read_text(encoding="utf-8"), escondido=True))

    # ── Fechamento ────────────────────────────────────────────────────────
    _, inovacao = secao(secoes, "🔎")
    _, alem = secao(secoes, "📚")
    _, checklist = secao(secoes, "✅")
    fechamento = f"## 🔎 Inovação OSINT do dia\n\n{inovacao}\n\n" if inovacao else ""
    fechamento += f"## 📚 Para ir além\n\n{alem}\n\n" if alem else ""
    fechamento += f"## ✅ Checklist\n\n{checklist}\n\n" if checklist else ""
    fechamento += (f"---\n\n🎉 Terminou? [Registre sua entrega do Dia {numero}]({URL_REPO}/issues/new?template=entreguei-o-dia.yml) "
                   f"· Baseado em [cipher387/python-for-OSINT-21-days]({URL_ORIGINAL}) (MIT) "
                   f"· Adaptação pt-BR: [{REPO_GITHUB}]({URL_REPO})")
    celulas.append(md(corrigir_links(fechamento, slug)))

    notebook = {
        "cells": celulas,
        "metadata": {
            "colab": {"provenance": [], "toc_visible": True, "name": f"Dia {numero:02d} — {meta['titulo']}"},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }
    destino = pasta / "notebook.ipynb"
    destino.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return destino, len(celulas)


if __name__ == "__main__":
    filtro = {int(a) for a in sys.argv[1:]}
    for meta in dias():
        if filtro and meta["dia"] not in filtro:
            continue
        destino, n = construir(meta)
        print(f"📓 {destino.relative_to(destino.parent.parent)} ({n} células)")
