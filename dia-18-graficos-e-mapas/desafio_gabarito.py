"""
Gabarito do Desafio S do Dia 18 — Mapa offline + distâncias.

Desenha um mapa das vítimas em SVG SEM internet e SEM biblioteca de mapas: converte
latitude/longitude em x/y (projeção equirretangular com correção pelo cosseno da latitude),
com círculos de área proporcional às vítimas. Calcula a distância (fórmula de haversine)
de cada cidade até o endereço do rodapé da loja (CEP 30130-010, centro de BH).
"""

import csv
import difflib
import html
import math
import unicodedata
from collections import Counter
from pathlib import Path

LARGURA_PX = 640  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"

COORDENADAS = {
    "Belo Horizonte": (-19.92, -43.94), "Betim": (-19.97, -44.20), "Contagem": (-19.93, -44.05),
    "Divinópolis": (-20.14, -44.89), "Governador Valadares": (-18.85, -41.95),
    "Ipatinga": (-19.47, -42.54), "Juiz de Fora": (-21.76, -43.35), "Poços de Caldas": (-21.79, -46.56),
    "Sete Lagoas": (-19.47, -44.25), "Uberaba": (-19.75, -47.93), "Uberlândia": (-18.92, -48.28),
}
# Centro de BH, região do CEP 30130-010 do rodapé (aproximado; ver Dia 5)
RODAPE = (-19.92, -43.94)


def chave(t):
    s = "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))
    return " ".join(s.casefold().split())


OFICIAIS = {chave(c): c for c in COORDENADAS}


def padronizar(cidade):
    k = chave(cidade)
    if k in OFICIAIS:
        return OFICIAIS[k]
    p = difflib.get_close_matches(k, OFICIAIS, n=1, cutoff=0.8)
    return OFICIAIS[p[0]] if p else cidade


def haversine_km(a, b):
    """Distância em linha reta sobre a esfera terrestre (raio médio 6371 km)."""
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as f:
    vitimas = Counter(padronizar(d["cidade"]) for d in csv.DictReader(f, delimiter=";"))

# ── Projeção: lon → x, lat → y ────────────────────────────────────────────
lats = [c[0] for c in COORDENADAS.values()]
lons = [c[1] for c in COORDENADAS.values()]
margem = 0.8                                        # graus de folga em volta
lat_min, lat_max = min(lats) - margem, max(lats) + margem
lon_min, lon_max = min(lons) - margem, max(lons) + margem
# Perto do Equador 1° de longitude ≈ 1° de latitude; em -20° ele "encolhe" pelo cosseno.
fator = math.cos(math.radians((lat_min + lat_max) / 2))
escala = LARGURA_PX / ((lon_max - lon_min) * fator)
altura_px = round((lat_max - lat_min) * escala)


def xy(lat, lon):
    x = (lon - lon_min) * fator * escala
    y = (lat_max - lat) * escala                    # y do SVG cresce para baixo: invertemos
    return x, y


maior = max(vitimas.values())
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{LARGURA_PX}" height="{altura_px + 30}" '
       f'font-family="system-ui, sans-serif">',
       f'<rect width="100%" height="100%" fill="#f4f7fb"/>',
       f'<text x="10" y="{altura_px + 20}" font-size="11" fill="#5b6475">'
       f'Projeção equirretangular · coordenadas aproximadas · círculo = área ∝ vítimas</text>']
xr, yr = xy(*RODAPE)
svg.append(f'<circle cx="{xr:.1f}" cy="{yr:.1f}" r="4" fill="black"><title>CEP do rodapé</title></circle>')

linhas = []
for cidade, qtd in vitimas.most_common():
    lat, lon = COORDENADAS[cidade]
    x, y = xy(lat, lon)
    r = 22 * math.sqrt(qtd / maior)
    dist = haversine_km(RODAPE, (lat, lon))
    linhas.append((dist, cidade, qtd))
    svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#b3261e" fill-opacity=".35" stroke="#b3261e">'
               f'<title>{html.escape(cidade)}: {qtd}</title></circle>')
    svg.append(f'<text x="{x + r + 3:.1f}" y="{y + 4:.1f}" font-size="12">{html.escape(cidade)} ({qtd})</text>')
svg.append("</svg>")

SAIDAS.mkdir(exist_ok=True)
(SAIDAS / "mapa_offline.svg").write_text("\n".join(svg), encoding="utf-8")

print("📏 Distância em linha reta até o endereço do rodapé (centro de BH):\n")
for dist, cidade, qtd in sorted(linhas):
    print(f"   {cidade:<22} {dist:6.0f} km  {'●' * qtd}")
longe = sum(q for d, _, q in linhas if d > 200)
print(f"\n🧭 {longe} de {sum(vitimas.values())} vítimas moram a mais de 200 km do 'endereço' da loja.")
print("   Ninguém iria buscar a compra lá: o endereço só existia para parecer confiável.")
print("💾 saidas/mapa_offline.svg gravado (abre sem internet).")
