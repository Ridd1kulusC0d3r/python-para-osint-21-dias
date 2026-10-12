# ──────────────────────────────────────────────────────────────────────────
# Título: Verificador de sintaxe offline (ast + py_compile)
# NÃO há código do autor neste dia: o Day 21 do curso do cipher387 só recomenda
# ferramentas (verificadores de sintaxe e de estilo online, ChatGPT, Stack Overflow...).
# Este arquivo é uma RECONSTRUÇÃO da prática proposta, feita para este repositório:
# em vez de colar o código num site, o próprio Python verifica a sintaxe, sem internet
# (e sem mandar o seu código para ninguém).
# Uso:  python nivel1_checar_sintaxe.py [arquivo.py ...]   (padrão: codigo_com_erro.py)
# ──────────────────────────────────────────────────────────────────────────

import ast                 # "árvore de sintaxe abstrata": o Python lê o código sem executá-lo
import py_compile          # compila para bytecode (.pyc), como o Python faz antes de rodar
import sys
import tempfile
from pathlib import Path

PASTA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
arquivos = [Path(a) for a in sys.argv[1:]] or [PASTA / "codigo_com_erro.py"]

com_erro = 0
for caminho in arquivos:
    codigo = caminho.read_text(encoding="utf-8")
    try:
        # ast.parse lê e entende a estrutura do código, mas NÃO executa nada.
        # Por isso é seguro usar até em código de origem duvidosa.
        arvore = ast.parse(codigo, filename=str(caminho))
    except SyntaxError as erro:
        com_erro += 1
        print(f"❌ {caminho.name}: erro de sintaxe na linha {erro.lineno}, coluna {erro.offset}")
        print(f"   Mensagem do Python: {erro.msg}")
        if erro.text:
            print(f"   {erro.text.rstrip()}")
            # Uma setinha embaixo do ponto exato do erro
            print("   " + " " * max((erro.offset or 1) - 1, 0) + "^")
        continue

    # Se passou no ast, contamos o que existe no arquivo (só para mostrar o que a árvore sabe).
    funcoes = [n.name for n in ast.walk(arvore) if isinstance(n, ast.FunctionDef)]
    importes = sorted({a.name.split(".")[0] for n in ast.walk(arvore) if isinstance(n, ast.Import) for a in n.names}
                      | {n.module.split(".")[0] for n in ast.walk(arvore) if isinstance(n, ast.ImportFrom) and n.module})
    # py_compile confirma compilando de verdade (num arquivo temporário, para não sujar a pasta).
    with tempfile.TemporaryDirectory() as tmp:
        py_compile.compile(str(caminho), cfile=str(Path(tmp) / "x.pyc"), doraise=True)
    print(f"✅ {caminho.name}: sintaxe ok · {len(codigo.splitlines())} linhas · "
          f"{len(funcoes)} funções · importa {', '.join(importes) or 'nada'}")

print(f"\n{len(arquivos)} arquivo(s) verificados, {com_erro} com erro de sintaxe.")
