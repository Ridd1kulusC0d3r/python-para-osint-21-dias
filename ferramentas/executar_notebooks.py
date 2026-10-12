"""
Executa os notebooks de verdade (com Jupyter) para garantir que nenhuma célula quebra.

    pip install nbclient nbformat ipykernel
    python ferramentas/executar_notebooks.py --offline        # pula as células do original
    python ferramentas/executar_notebooks.py                  # tudo, com internet (CI semanal)

Sai com código 1 se alguma célula falhar.
"""

import argparse
import copy
import os
import sys
import time

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

from comum import dias


def preparar(nb, offline):
    """No modo offline, remove as células que dependem de pip/internet (o nível 1 original)."""
    nb = copy.deepcopy(nb)
    if offline:
        nb.cells = [c for c in nb.cells if not (c.cell_type == "code" and (
            "%cd -q {PASTA_NB}/original" in c.source or "%pip install" in c.source))]
    return nb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("dias", nargs="*", type=int)
    args = parser.parse_args()
    if args.offline:
        os.environ["OSINT_OFFLINE"] = "1"

    falhas = 0
    for meta in dias():
        if args.dias and meta["dia"] not in args.dias:
            continue
        caminho = meta["_pasta"] / "notebook.ipynb"
        if not caminho.exists():
            continue
        nb = preparar(nbformat.read(caminho, as_version=4), args.offline)
        inicio = time.time()
        try:
            NotebookClient(nb, timeout=180, kernel_name="python3",
                           resources={"metadata": {"path": str(meta["_pasta"])}}).execute()
            print(f"✅ Dia {meta['dia']:02d}  {time.time() - inicio:5.1f}s")
        except CellExecutionError as erro:
            falhas += 1
            print(f"❌ Dia {meta['dia']:02d}\n{str(erro)[-1500:]}")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
