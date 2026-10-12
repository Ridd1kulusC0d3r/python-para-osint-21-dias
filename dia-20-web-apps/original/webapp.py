# ──────────────────────────────────────────────────────────────────────────
# Título: Um web app mínimo com Streamlit
# Código ORIGINAL de cipher387 (Cyb_detective), "Python for OSINT. 21-day course"
# Fonte: https://github.com/cipher387/python-for-OSINT-21-days/blob/main/Day_20/webapp.py
# Licença: MIT © 2023 Cyb_detective. O código está intacto; só foram
# acrescentados comentários em pt-BR (linhas que começam com "# 💬").
# Requer: pip install streamlit · Rode com: streamlit run webapp.py (não com python)
# ──────────────────────────────────────────────────────────────────────────
# 💬 Streamlit transforma um script Python em página web. Cada clique RODA O SCRIPT DE NOVO.
import streamlit as st

# 💬 Título grande no topo da página.
st.title("Simple web app")


# 💬 Caixa de texto; o segundo argumento é o valor inicial.
textInput = st.text_input("Enter some text", "…")

# 💬 st.button devolve True só na rodada em que foi clicado.
if(st.button("Start")):
    # 💬 Esta variável é calculada mas nunca usada (resto de uma versão anterior, talvez).
    nickname = textInput.title()
    # 💬 Mostra o texto na página. O Streamlit escapa o HTML para você.
    st.text("You entered: "+textInput)
