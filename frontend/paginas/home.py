import streamlit as st
from backend.banco_de_dados import Banco

st.set_page_config(page_title="Home", page_icon="frontend/imagens/pref_icone.ico")
st.title("EGGEM (Home)")
#st.text(type(st.session_state.get("token").encode('utf-8')))
#st.write(st.session_state.get("token"))
#informacoes = Banco().get_informacoes("5")
#st.write("tipo:", informacoes[0])