"""
Mapa interativo das vítimas com Leaflet, gerado só com strings.

Carta 39 (rank A) — Jutsu do Mapa das Vítimas (parte 3)

O que você aprende:
  • a escrever uma página HTML que carrega o Leaflet (biblioteca de mapas em JavaScript) por CDN;
  • a passar dados do Python para o JavaScript com json.dumps (sem montar texto na mão);
  • a desenhar círculos com área proporcional ao número de vítimas (raiz quadrada!).

As coordenadas são APROXIMADAS (centro de cada município), embutidas no script: suficiente para
um mapa de distribuição, nunca para localizar uma pessoa.

Como rodar (dentro da pasta dia-18-graficos-e-mapas):
    python br/03_mapa_leaflet.py
    (abra saidas/mapa_vitimas.html no navegador: precisa de internet para baixar o mapa de fundo)
"""

import csv
import difflib
import json
import math
import unicodedata
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

# ── Parâmetros ────────────────────────────────────────────────────────────
RAIO_MAXIMO_KM = 30  #@param {type:"integer"}

PASTA_DIA = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
PASTA_CASO = PASTA_DIA.parent / "caso" / "dados"
SAIDAS = PASTA_DIA / "saidas"

# Centro aproximado de cada município (latitude, longitude), arredondado.
COORDENADAS = {
    "Belo Horizonte": (-19.92, -43.94),
    "Betim": (-19.97, -44.20),
    "Contagem": (-19.93, -44.05),
    "Divinópolis": (-20.14, -44.89),
    "Governador Valadares": (-18.85, -41.95),
    "Ipatinga": (-19.47, -42.54),
    "Juiz de Fora": (-21.76, -43.35),
    "Poços de Caldas": (-21.79, -46.56),
    "Sete Lagoas": (-19.47, -44.25),
    "Uberaba": (-19.75, -47.93),
    "Uberlândia": (-18.92, -48.28),
}


def chave(texto):
    sem = "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))
    return " ".join(sem.casefold().split())


CHAVES_OFICIAIS = {chave(c): c for c in COORDENADAS}


def padronizar(cidade):
    k = chave(cidade)
    if k in CHAVES_OFICIAIS:
        return CHAVES_OFICIAIS[k]
    parecidas = difflib.get_close_matches(k, CHAVES_OFICIAIS, n=1, cutoff=0.8)
    return CHAVES_OFICIAIS[parecidas[0]] if parecidas else cidade


# ── 1. Agregar por cidade ─────────────────────────────────────────────────
vitimas = Counter()
prejuizo = defaultdict(Decimal)
with open(PASTA_CASO / "denuncias.csv", encoding="utf-8") as arquivo:
    for d in csv.DictReader(arquivo, delimiter=";"):
        cidade = padronizar(d["cidade"])
        vitimas[cidade] += 1
        prejuizo[cidade] += Decimal(d["valor"])

sem_coordenada = [c for c in vitimas if c not in COORDENADAS]
if sem_coordenada:
    print(f"⚠️ Sem coordenada (ficam fora do mapa): {sem_coordenada}")

# ── 2. Tamanho do círculo ─────────────────────────────────────────────────
# Nosso olho compara ÁREAS, não raios. Se uma cidade tem 4x mais vítimas, o círculo dela
# deve ter 4x mais área, ou seja, raio 2x maior. Por isso usamos a raiz quadrada.
maior = max(vitimas.values())
pontos = []
for cidade, qtd in vitimas.most_common():
    if cidade not in COORDENADAS:
        continue
    lat, lon = COORDENADAS[cidade]
    raio_m = RAIO_MAXIMO_KM * 1000 * math.sqrt(qtd / maior)
    total = f"{prejuizo[cidade]:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")
    pontos.append({"cidade": cidade, "lat": lat, "lon": lon, "vitimas": qtd,
                   "raio": round(raio_m), "prejuizo": f"R$ {total}"})
    print(f"📍 {cidade:<22} {qtd:>2} vítimas · raio {raio_m / 1000:5.1f} km · R$ {total}")

# ── 3. A página ───────────────────────────────────────────────────────────
# json.dumps transforma a lista Python em texto JavaScript válido (aspas, acentos, tudo certo).
# Leaflet 1.9.4 via unpkg, com versão fixa (nunca "latest": a página não muda sozinha amanhã).
pagina = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mapa das vítimas — Operação Vitrine Fantasma</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>html, body, #mapa { height: 100%; margin: 0; } .caixa { font: 14px system-ui; }</style>
</head>
<body>
<div id="mapa"></div>
<script>
const pontos = __PONTOS__;
const mapa = L.map("mapa").setView([-19.9, -44.5], 7);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 18,
  attribution: "&copy; colaboradores do OpenStreetMap"
}).addTo(mapa);
for (const p of pontos) {
  L.circle([p.lat, p.lon], {radius: p.raio, color: "#b3261e", fillOpacity: 0.35})
    .bindPopup(`<div class="caixa"><b>${p.cidade}</b><br>${p.vitimas} vítima(s)<br>${p.prejuizo}</div>`)
    .addTo(mapa);
}
const grupo = L.featureGroup(pontos.map(p => L.marker([p.lat, p.lon])));
mapa.fitBounds(grupo.getBounds().pad(0.2));
</script>
</body>
</html>
""".replace("__PONTOS__", json.dumps(pontos, ensure_ascii=False))
# Usamos .replace em vez de f-string porque o JavaScript está cheio de chaves { }.
# Os dados (nomes de cidade) vêm do NOSSO dicionário, não de terceiros. Se viessem
# de fora, seria preciso escapar o HTML no popup (ver Dia 20, XSS).

SAIDAS.mkdir(exist_ok=True)
destino = SAIDAS / "mapa_vitimas.html"
destino.write_text(pagina, encoding="utf-8")
print(f"\n🗺️ {destino.relative_to(PASTA_DIA)} gravado com {len(pontos)} cidades.")
print("💡 Abra no navegador (precisa de internet para o mapa de fundo e o Leaflet).")

# No Colab/Jupyter, mostra o mapa abaixo da célula.
if "__file__" not in globals():
    try:
        from IPython.display import HTML, display
        display(HTML(f'<iframe srcdoc="{pagina.replace(chr(34), "&quot;")}" width="100%" height="500"></iframe>'))
    except ImportError:
        pass
