"""
Funções compartilhadas pelas ferramentas do repositório (só biblioteca padrão).

Não é material de estudo: é a "oficina" que gera notebooks, cartas e o site
a partir dos arquivos de cada dia.
"""

import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REPO_GITHUB = "Ridd1kulusC0d3r/python-para-osint-21-dias"
URL_REPO = f"https://github.com/{REPO_GITHUB}"
URL_ORIGINAL = "https://github.com/cipher387/python-for-OSINT-21-days"

RANK_COR = {  # cores das bordas das cartas por rank
    "D": "#8a8f98", "C": "#3fa66b", "B": "#3b82c4", "A": "#8b5cf6", "S": "#e0a400",
}
NIVEL_NOME = {1: "Original · cipher387", 2: "Camada Brasil", 3: "Desafio"}


def dias():
    """Lista as pastas dia-XX-* em ordem, com o dia.json já carregado."""
    saida = []
    for pasta in sorted(RAIZ.glob("dia-[0-9][0-9]-*")):
        meta_arq = pasta / "dia.json"
        if meta_arq.exists():
            meta = json.loads(meta_arq.read_text(encoding="utf-8"))
            meta["_pasta"] = pasta
            saida.append(meta)
    return saida


def secoes_markdown(texto):
    """Divide um README em {título da seção '## ...': conteúdo}."""
    secoes, atual, linhas = {}, "_topo", []
    for linha in texto.splitlines():
        if linha.startswith("## "):
            secoes[atual] = "\n".join(linhas).strip()
            atual, linhas = linha[3:].strip(), []
        else:
            linhas.append(linha)
    secoes[atual] = "\n".join(linhas).strip()
    return secoes


def secao(secoes, prefixo):
    """Devolve o conteúdo da primeira seção cujo título começa com `prefixo`."""
    for titulo, conteudo in secoes.items():
        if titulo.startswith(prefixo):
            return titulo, conteudo
    return None, ""


def entre_marcadores(texto, nome):
    """Texto entre <!-- nome:inicio --> e <!-- nome:fim -->."""
    m = re.search(rf"<!--\s*{nome}:inicio\s*-->(.*?)<!--\s*{nome}:fim\s*-->", texto, re.S)
    return m.group(1).strip() if m else ""


def titulo_do_script(caminho):
    """Primeira linha da docstring (br/) ou a linha '# Título:' (original/)."""
    texto = caminho.read_text(encoding="utf-8")
    m = re.search(r"^#\s*Título:\s*(.+)$", texto, re.M)
    if m:
        return m.group(1).strip()
    m = re.match(r'\s*(?:"""|\'\'\')\s*\n?(.+)', texto)
    if m:
        return m.group(1).strip()
    return caminho.stem
