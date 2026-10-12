# ──────────────────────────────────────────────────────────────────────────
# Título: Gráfico de barras com Matplotlib
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_18/bar.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install matplotlib  (o numpy vem junto)
# ──────────────────────────────────────────────────────────────────────────
# 💬 pyplot é a parte do Matplotlib que desenha gráficos, apelidada de plt.
import matplotlib.pyplot as plt
# 💬 numpy: listas numéricas rápidas (arrays). Aqui só embrulha as listas.
import numpy as np

# 💬 Rótulos das barras (eixo x).
x = np.array(["Los Angeles", "San Francisco", "New York"])
# 💬 Altura de cada barra: população em milhões.
y = np.array([3.8, 0.8, 8.4])

# 💬 Desenha as barras.
plt.bar(x,y)

plt.title ("Population")

# 💬 Grava a imagem PNG na pasta atual.
plt.savefig('population_barchart.png')
