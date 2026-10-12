"""
Ler os depoimentos: abrir vários arquivos de texto, contar linhas e palavras.

Carta 25 (rank B) — Jutsu dos Depoimentos (parte 1)

O que você aprende:
  • a abrir arquivos com "with open(..., encoding='utf-8')" (fecha sozinho e não estraga acentos);
  • as três formas de ler: read() (tudo), readlines() (lista de linhas) e "for linha in arquivo";
  • a achar vários arquivos de uma vez com glob("*.txt");
  • a contar linhas, palavras e caracteres e a montar uma tabela-resumo.

Os depoimentos ficam em caso/dados/depoimentos/ (fictícios). Este script não usa internet.

Como rodar (dentro da pasta dia-04-arquivos):
    python br/01_ler_depoimentos.py
"""

from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
MOSTRAR_PRIMEIRO_INTEIRO = True  #@param {type:"boolean"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_DEPOIMENTOS = PASTA_DIA.parent / "caso" / "dados" / "depoimentos"

# ── 1. Achar os arquivos ──────────────────────────────────────────────────
# glob("*.txt") devolve todos os arquivos que terminam em .txt; sorted() põe em ordem.
arquivos = sorted(PASTA_DEPOIMENTOS.glob("*.txt"))
print(f"📂 {len(arquivos)} depoimentos em {PASTA_DEPOIMENTOS.relative_to(PASTA_DIA.parent)}\n")

# ── 2. Forma 1: read() — o arquivo inteiro num texto só ───────────────────
if MOSTRAR_PRIMEIRO_INTEIRO and arquivos:
    # "with" abre e FECHA o arquivo no fim do bloco, mesmo se acontecer um erro no meio.
    # encoding="utf-8": os depoimentos têm acentos ("Vítima", "Divinópolis").
    with open(arquivos[0], "r", encoding="utf-8") as arquivo:
        texto = arquivo.read()
    print(f"📄 {arquivos[0].name} (lido com read()):")
    print("   " + texto.strip().replace("\n", "\n   "))
    print()

# ── 3. Forma 2: readlines() — uma lista de linhas ─────────────────────────
with open(arquivos[0], encoding="utf-8") as arquivo:
    linhas = arquivo.readlines()
# Cada item termina com "\n" (a quebra de linha). strip() tira isso e os espaços das pontas.
print(f"🔢 readlines() devolveu {len(linhas)} itens. O primeiro, como o Python vê: {linhas[0]!r}")
print(f"   A linha [1] (a segunda) sem o \\n: {linhas[1].strip()!r}\n")

# ── 4. Forma 3: for linha in arquivo — uma linha por vez, para cada depoimento ──
print(f"{'Arquivo':<12} {'Linhas':>6} {'Vazias':>6} {'Palavras':>8} {'Caracteres':>10}")
print("─" * 48)
total_palavras = 0
for caminho in arquivos:
    n_linhas = 0
    n_vazias = 0
    n_palavras = 0
    n_caracteres = 0
    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:                   # lê uma linha de cada vez (bom para arquivos enormes)
            n_linhas += 1
            if not linha.strip():               # linha que só tem espaço ou "\n" conta como vazia
                n_vazias += 1
            n_palavras += len(linha.split())    # split() sem nada separa por qualquer espaço
            n_caracteres += len(linha.rstrip("\n"))
    total_palavras += n_palavras
    print(f"{caminho.name:<12} {n_linhas:>6} {n_vazias:>6} {n_palavras:>8} {n_caracteres:>10}")

print("─" * 48)
media = total_palavras / len(arquivos) if arquivos else 0
print(f"📊 Total: {total_palavras} palavras · média de {media:.1f} por depoimento")

# ── 5. Uma busca simples: em quantos depoimentos aparece "Kau"? ───────────
# "in" num texto responde se um pedaço aparece dentro dele.
com_kau = [c.name for c in arquivos if "Kau" in c.read_text(encoding="utf-8")]
print(f"🕵️  'Kau' aparece em {len(com_kau)} de {len(arquivos)} depoimentos: {', '.join(com_kau)}")
