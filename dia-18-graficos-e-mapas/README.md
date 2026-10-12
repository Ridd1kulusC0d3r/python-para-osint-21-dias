# Dia 18 — Gerando gráficos e mapas

> 🃏 Cartas **18 · 39 · 60**  ·  📘 Original: *Day 18. Generating charts and maps*

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ridd1kulusC0d3r/python-para-osint-21-dias/blob/main/dia-18-graficos-e-mapas/notebook.ipynb)

## 📖 Capítulo 18 — Onde estão as vítimas

<!-- historia:inicio -->
A Delegada Rita leu o relatório preliminar e devolveu com uma única anotação a caneta, na margem da
tabela de denúncias: *"E no mapa?"*

A Iara ri.

— Toda autoridade é assim. Ninguém lê tabela de 37 linhas. Uma imagem decide em três segundos se o
caso é da delegacia do bairro ou de uma força-tarefa estadual.

Ela abre o mapa de Minas na parede e começa a espetar alfinetes nas cidades que você listou: Belo
Horizonte, Contagem, Uberlândia, Juiz de Fora, Governador Valadares... Na quinta cidade, para.

— Está vendo o desenho? Se o golpe fosse de bairro, os alfinetes estariam todos juntos. Estão
espalhados pelo estado inteiro. Isso é anúncio pago em rede social, grupo de promoção, coisa que
viaja longe. E repare: o endereço do rodapé fica no centro de BH, mas tem vítima a quase 500
quilômetros dali.

Ela devolve a caneta para você.

— Faça três versões: uma para o terminal, que é rápida; uma imagem, para o relatório; e um mapa de
verdade, para a doutora clicar.
<!-- historia:fim -->

## 🎯 Objetivos

- Fazer um gráfico de barras com `matplotlib` e um mapa com `Basemap`, como no curso original.
- Conhecer uma alternativa leve e interativa ao Basemap (`folium`).
- Desenhar gráficos no **terminal** e em **SVG** só com a biblioteca padrão.
- Gerar um mapa interativo com **Leaflet** a partir do Python.
- Usar área proporcional (raiz quadrada) para não enganar o leitor.

## 🧠 Conceito em 2 minutos

<!-- conceito:inicio -->
Um gráfico é só uma **regra que transforma número em tamanho**: o maior valor ganha a barra mais
comprida, e os outros, uma fração dela (regra de três). Isso funciona igual no terminal (quantos
`▇`), no SVG (quantos pixels) ou no matplotlib.

**SVG** é uma imagem feita de texto: `<rect x="10" y="20" width="80" height="22"/>` é um retângulo.
Como é texto, o Python escreve SVG com f-strings, e o arquivo abre em qualquer navegador. Cuidado:
no SVG o eixo **y cresce para baixo**.

**Mapa** é um gráfico em que x e y são longitude e latitude. Duas armadilhas:

| Armadilha | Como evitar |
|---|---|
| Ordem das coordenadas | Basemap e GeoJSON usam **(lon, lat)**; folium e Leaflet usam **[lat, lon]** |
| Círculo proporcional | o olho compara **áreas**: raio ∝ √valor (4x vítimas = raio 2x) |

**Leaflet** é uma biblioteca JavaScript de mapas. O Python só escreve o HTML com os dados embutidos
(via `json.dumps`), e o navegador faz o resto, usando os "azulejos" (*tiles*) do OpenStreetMap como
fundo.
<!-- conceito:fim -->

## 🥋 Nível 1 — Exercício original (cipher387)

| Arquivo | O que faz |
|---|---|
| [`original/bar.py`](original/bar.py) | Gráfico de barras da população de três cidades dos EUA (`matplotlib` + `numpy`) |
| [`original/map.py`](original/map.py) | Mapa-múndi com fronteiras, costas e um ponto (`Basemap`) |
| [`original/2026_map.py`](original/2026_map.py) | **Alternativa 2026:** o mesmo ponto num mapa interativo com `folium` |

```bash
pip install matplotlib basemap folium
cd dia-18-graficos-e-mapas/original
python bar.py          # gera population_barchart.png
python map.py          # gera map.png (demora um pouco: Basemap é pesado)
python 2026_map.py     # gera map.html (abra no navegador)
```

> ℹ️ **Basemap em 2026.** Ele ainda instala com `pip install basemap` (o pacote traz os dados de
> costas e fronteiras em `basemap_data`) e o `map.py` original continua funcionando. Mas o projeto
> vive em modo de manutenção, e a própria documentação dele aponta o **Cartopy** como sucessor. Para OSINT,
> onde um mapa clicável costuma valer mais que uma imagem, o `folium` é a troca mais simples.

> 🔍 No `map.py`, o ponto `plot(43.00, 39.00)` é **longitude 43, latitude 39** (leste da Turquia).
> Troque a ordem (lon 39, lat 43) e o ponto cai no Mar Negro. É o erro mais comum com mapas.

No Colab, o PNG aparece com `from IPython.display import Image; Image("map.png")`, e o folium aparece
só de escrever o nome da variável do mapa na última linha da célula.

## 🇧🇷 Nível 2 — Camada Brasil

Só **biblioteca padrão**, 100% offline para gerar (o mapa Leaflet precisa de internet só na hora de
**abrir**, para baixar o fundo).

| Arquivo | O que faz |
|---|---|
| [`br/01_grafico_terminal.py`](br/01_grafico_terminal.py) | Barras `▇` no terminal: vítimas (ou prejuízo) por cidade padronizada |
| [`br/02_grafico_svg.py`](br/02_grafico_svg.py) | `saidas/vitimas_por_cidade.svg` desenhado só com strings, com grade e dicas ao passar o mouse |
| [`br/03_mapa_leaflet.py`](br/03_mapa_leaflet.py) | `saidas/mapa_vitimas.html` com Leaflet 1.9.4 (unpkg) e círculos de área proporcional |

```bash
cd dia-18-graficos-e-mapas
python br/01_grafico_terminal.py
python br/03_mapa_leaflet.py       # depois abra saidas/mapa_vitimas.html
```

No Colab, os scripts 02 e 03 mostram a imagem e o mapa logo abaixo da célula (com
`IPython.display`, protegido por `try/except ImportError` para não quebrar fora do notebook).

**O que você deve ver no caso:** depois de padronizadas, as 16 grafias viram **11 cidades**. Belo
Horizonte lidera com 8 vítimas, mas a Grande BH (BH, Contagem e Betim) soma só 38% do total. O resto
está espalhado do Triângulo Mineiro ao Vale do Rio Doce.

## ⚖️ Ética, LGPD e OPSEC

- **Agregue antes de mapear.** O mapa mostra **cidades**, nunca endereços de vítimas. Ponto exato de
  pessoa num mapa é dado pessoal sensível na prática (permite achar a casa de alguém).
- **Cuidado com cidades pequenas.** "1 vítima em uma cidade de 3 mil habitantes" pode identificar a
  pessoa. Em relatórios públicos, agrupe por região quando a contagem for muito baixa.
- **Mapa online vaza.** O HTML com Leaflet baixa azulejos do OpenStreetMap: o servidor do mapa vê seu
  IP e a região que você está olhando. Para casos sensíveis, prefira o mapa offline do desafio.
- **Gráfico também mente.** Barra que não começa no zero, círculo com raio (e não área)
  proporcional, cores alarmistas: tudo isso distorce. Relatório de investigação tem que ser sóbrio.
- Os azulejos do OpenStreetMap têm política de uso: atribuição obrigatória e nada de baixar em massa.

## 🏆 Nível 3 — Desafio S

[`desafio.md`](desafio.md) — **Mapa offline + distâncias**: projetar lat/lon em SVG sem internet e
calcular a distância de cada cidade até o endereço do rodapé com a fórmula de haversine.

## 🔎 Inovação OSINT do dia

**Overture Maps: base aberta de lugares do mundo, com cliente Python.** A Overture Maps Foundation
(Linux Foundation, com Amazon, Meta, Microsoft e TomTom) publica dados abertos de lugares
(estabelecimentos), prédios, endereços e vias. O cliente `pip install overturemaps` baixa só uma
região: `overturemaps download --bbox=oeste,sul,leste,norte -f geojson --type=place -o lugares.geojson`
(atenção à ordem: longitude, latitude). Em OSINT, serve para checar se um "endereço comercial" de uma
loja suspeita corresponde a algum estabelecimento conhecido naquele quarteirão, sem raspar nenhum
site. O GeoJSON resultante abre direto no folium ou no Leaflet.

## 📚 Para ir além

- Leaflet (tutoriais em inglês, muito visuais): <https://leafletjs.com/examples.html>
- folium: <https://python-visualization.github.io/folium/>
- Basemap (status e instalação): <https://matplotlib.org/basemap/>
- Cartopy: <https://scitools.org.uk/cartopy/>
- Política de uso dos azulejos do OpenStreetMap: <https://operations.osmfoundation.org/policies/tiles/>
- Cliente Python do Overture Maps: <https://docs.overturemaps.org/getting-data/overturemaps-py/>
- Malhas municipais oficiais do IBGE (para mapas com contorno das cidades): <https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais.html>

## ✅ Checklist

- [ ] Rodei `bar.py` e `map.py` (ou o `2026_map.py`)
- [ ] Entendi a diferença entre (lon, lat) e [lat, lon]
- [ ] Vi o gráfico de barras no terminal
- [ ] Abri o SVG no navegador e passei o mouse nas barras
- [ ] Abri o mapa Leaflet e cliquei nas cidades
- [ ] Fiz o desafio S
- [ ] Anotei no meu [`DIARIO.md`](../DIARIO.md)
