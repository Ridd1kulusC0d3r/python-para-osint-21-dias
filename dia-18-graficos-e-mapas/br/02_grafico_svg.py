"""
Gráfico de barras em SVG gerado só com strings (sem matplotlib).

Carta 39 (rank A) — Jutsu do Mapa das Vítimas (parte 2)

O que você aprende:
  • que SVG é uma imagem feita de TEXTO (retângulos, linhas, textos com coordenadas);
  • a converter números em pixels (escala) e a lembrar que o eixo y do SVG cresce para BAIXO;
  • a gravar um arquivo .svg que abre no navegador, no Word e no GitHub.

Como rodar (dentro da pasta dia-18-graficos-e-mapas):
    python br/02_grafico_svg.py
    (depois abra saidas/vitimas_por_cidade.svg no navegador)
"""

import csv
import difflib
import html
import unicodedata
from collections import Counter
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
TITULO = "Operação Vitrine Fantasma — vítimas por cidade"  #@param {type:"string"}
COR_BARRA = "#1f5fa8"  #@param {type:"string"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"

OFICIAIS = ["Belo Horizonte", "Betim", "Contagem", "Divinópolis", "Governador Valadares",
            "Ipatinga", "Juiz de Fora", "Poços de Caldas", "Sete Lagoas", "Uberaba", "Uberlândia"]


def chave(texto):
    sem = "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))
    return " ".join(sem.casefold().split())


CHAVES_OFICIAIS = {chave(c): c for c in OFICIAIS}


def padronizar(cidade):
    k = chave(cidade)
    if k in CHAVES_OFICIAIS:
        return CHAVES_OFICIAIS[k]
    parecidas = difflib.get_close_matches(k, CHAVES_OFICIAIS, n=1, cutoff=0.8)
    return CHAVES_OFICIAIS[parecidas[0]] if parecidas else cidade


# ── 1. Dados ──────────────────────────────────────────────────────────────
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    contagem = Counter(padronizar(d["cidade"]) for d in csv.DictReader(arquivo, delimiter=";"))
itens = contagem.most_common()                 # [("Belo Horizonte", 8), ...]

# ── 2. Geometria (tudo em pixels) ─────────────────────────────────────────
# Barras HORIZONTAIS: nomes de cidade longos cabem melhor à esquerda.
MARGEM_ESQ, MARGEM_TOPO = 170, 60              # espaço para os nomes e para o título
ALTURA_BARRA, ESPACO = 22, 8
LARGURA_UTIL = 420                             # largura da barra mais comprida
largura = MARGEM_ESQ + LARGURA_UTIL + 60
altura = MARGEM_TOPO + len(itens) * (ALTURA_BARRA + ESPACO) + 40
maior = itens[0][1]


def escala(valor):
    """Converte 'número de vítimas' em 'pixels de largura'."""
    return valor / maior * LARGURA_UTIL


# ── 3. Desenhar: cada elemento é uma linha de texto ───────────────────────
partes = [
    # viewBox define o sistema de coordenadas; width/height o tamanho na tela.
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" '
    f'viewBox="0 0 {largura} {altura}" font-family="system-ui, sans-serif">',
    f'<rect width="{largura}" height="{altura}" fill="white"/>',
    f'<text x="20" y="32" font-size="18" font-weight="bold" fill="#1d2433">{html.escape(TITULO)}</text>',
]

# Linhas de grade verticais a cada 2 vítimas (ajudam a ler o valor)
for marca in range(0, maior + 1, 2):
    x = MARGEM_ESQ + escala(marca)
    partes.append(f'<line x1="{x:.1f}" y1="{MARGEM_TOPO - 8}" x2="{x:.1f}" y2="{altura - 30}" stroke="#e3e7ee"/>')
    partes.append(f'<text x="{x:.1f}" y="{altura - 12}" font-size="11" fill="#5b6475" text-anchor="middle">{marca}</text>')

for i, (cidade, valor) in enumerate(itens):
    # No SVG, y=0 é o TOPO. Cada barra desce (ALTURA_BARRA + ESPACO) pixels em relação à anterior.
    y = MARGEM_TOPO + i * (ALTURA_BARRA + ESPACO)
    meio = y + ALTURA_BARRA / 2 + 4             # +4: centraliza o texto na barra visualmente
    partes.append(f'<text x="{MARGEM_ESQ - 10}" y="{meio:.1f}" font-size="13" text-anchor="end" '
                  f'fill="#1d2433">{html.escape(cidade)}</text>')
    partes.append(f'<rect x="{MARGEM_ESQ}" y="{y}" width="{escala(valor):.1f}" height="{ALTURA_BARRA}" '
                  f'rx="3" fill="{html.escape(COR_BARRA)}"><title>{html.escape(cidade)}: {valor}</title></rect>')
    # <title> dentro do retângulo vira "dica" quando você passa o mouse por cima.
    partes.append(f'<text x="{MARGEM_ESQ + escala(valor) + 6:.1f}" y="{meio:.1f}" font-size="12" '
                  f'fill="#1d2433">{valor}</text>')

partes.append("</svg>")
svg = "\n".join(partes)

SAIDAS.mkdir(exist_ok=True)
destino = SAIDAS / "vitimas_por_cidade.svg"
destino.write_text(svg, encoding="utf-8")
print(f"🖼️ {destino.relative_to(PASTA_DIA)} gravado: {len(itens)} barras, {largura}x{altura} px, {len(svg)} caracteres.")
print("💡 Abra no navegador. Dá para colar no relatório HTML do Dia 17 (SVG é texto, cabe dentro do HTML).")

# No Colab/Jupyter, mostra a imagem abaixo da célula.
if "__file__" not in globals():
    try:
        from IPython.display import SVG, display
        display(SVG(svg))
    except ImportError:
        pass
