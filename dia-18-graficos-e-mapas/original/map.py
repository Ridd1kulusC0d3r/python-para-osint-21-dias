# ──────────────────────────────────────────────────────────────────────────
# Título: Mapa-múndi com Basemap
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_18/map.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install basemap  (pacote pesado; veja a alternativa 2026_map.py)
# ──────────────────────────────────────────────────────────────────────────
import numpy as np
import matplotlib.pyplot as plt
# 💬 Basemap é um complemento do Matplotlib para mapas. Vive em modo de
# 💬 manutenção; a documentação dele aponta o Cartopy como sucessor.
from mpl_toolkits.basemap import Basemap

# 💬 Uma figura grande: 22 x 22 polegadas.
fig = plt.figure(figsize = (22,22)) 

# 💬 Sem argumentos = mapa-múndi em projeção cilíndrica simples (lon/lat).
map = Basemap()

# 💬 Fronteiras dos países e, abaixo, as linhas de costa.
map.drawcountries()
map.drawcoastlines()

# 💬 Um ponto azul ('b' = blue, 'o' = bolinha). A ordem é LONGITUDE, LATITUDE:
# 💬 43 °E, 39 °N cai na região leste da Turquia. Confundir a ordem é o erro nº 1 com mapas.
map.plot(43.00, 39.00, 'bo', markersize=12)

plt.title("World map", fontsize=20)

# 💬 Grava o mapa como imagem.
plt.savefig('map.png')
