import streamlit as st
import time
import requests
from frontend.funcoes_paginas import criar_botao_home
from frontend.controle_autenticacao import verificar_token
from fastapi import HTTPException


def exibir_pagina_login():

    st.set_page_config(page_title="Login", page_icon="frontend/imagens/pref_icone.ico")
    criar_botao_home()

    if verificar_token():
        st.error("Usuário já logado.")
        return

    url_imagem_github = "https://raw.githubusercontent.com/Ozen-ok2/teste-imagens/main/imagem_central.jpeg"
    st.markdown(
        f'<img src="{url_imagem_github}" alt="Imagem" style="display:block; margin:auto;">',
        unsafe_allow_html=True,
    )

    st.title("Login")
    usuario = st.text_input("Usuário:")
    senha = st.text_input("Senha:", type="password")

    col1, col2 = st.columns([0.12, 0.88])

    if col1.button("Entrar"):
        if usuario and senha:
            dados_login = {"usuario": usuario, "senha": senha}
            try:
                response = requests.post("http://localhost:5000/login", json=dados_login)
                response.raise_for_status()  # Lança uma exceção HTTPException se a resposta não for bem-sucedida (status diferente de 2xx)
                
                dados_resposta = response.json()
                st.session_state.token = dados_resposta["token"]
                with st.spinner("Realizando login..."):
                    time.sleep(3)
                st.success(dados_resposta["mensagem"])
                st.toast("Redirecionando para o informativo sobre as ações.")
                time.sleep(3)
                st.session_state.authenticated = True
                st.switch_page("paginas/home.py")
    
            except requests.exceptions.HTTPError as http_error:
                status_code = http_error.response.status_code
                if status_code == 401:
                    st.error("Erro ao fazer login: Credenciais inválidas. Acesso negado.")
                elif status_code == 500:
                    st.error("Erro ao fazer login: Erro interno do servidor.")
                else:
                    st.error(f"Erro ao fazer login: {status_code}")
            except Exception as e:
                st.error(f"Erro ao fazer login: não foi possível se conectar ao servidor.")
        else:
            st.warning("Preencha todos os campos.")

    if st.button("Não possui uma conta?"):
        st.switch_page("paginas/criar_conta.py")

    if col2.button("Esqueceu a senha?"):
        st.switch_page("paginas/esqueceu_a_senha.py")


exibir_pagina_login()
