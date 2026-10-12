# ──────────────────────────────────────────────────────────────────────────
# Título: O mesmo mapa com folium (alternativa leve, 2026)
# ATUALIZAÇÃO 2026 feita para este repositório, BASEADA no original de cipher387
# (Day_18/map.py, MIT © 2023 Cyb_detective). O original continua intacto em map.py
# e ainda funciona (pip install basemap). Esta versão existe porque o Basemap é
# pesado, está em modo de manutenção e gera só imagem parada. O folium gera um mapa
# INTERATIVO em HTML (zoom, arrastar, clicar no ponto), sobre o OpenStreetMap.
# Requer: pip install folium
# ──────────────────────────────────────────────────────────────────────────

# 💬 folium escreve um HTML que usa a biblioteca JavaScript Leaflet.
import folium

# 💬 Mapa-múndi: centro em (lat 20, lon 0) e zoom 2 (bem afastado).
mapa = folium.Map(location=[20, 0], zoom_start=2)

# 💬 O mesmo ponto do original. ATENÇÃO à ordem: o Basemap recebe (longitude, latitude),
# 💬 o folium recebe [latitude, longitude]. Original: plot(43.00, 39.00) = lon 43, lat 39.
folium.CircleMarker(location=[39.00, 43.00], radius=10, color="blue", fill=True,
                    popup="lat 39, lon 43 (leste da Turquia)").add_to(mapa)

# 💬 Grava o HTML. Abra no navegador (ou, no Colab/Jupyter, só escreva "mapa" numa célula).
mapa.save("map.html")
print("map.html gravado")
