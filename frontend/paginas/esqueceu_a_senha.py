import streamlit as st, time, requests
from funcoes_paginas import criar_botao_home


def exibir_pagina_esqueceu_senha():

    st.set_page_config(
        page_title="Esqueceu a senha", page_icon="frontend/imagens/pref_icone.ico"
    )

    criar_botao_home()

    st.title("Esqueceu a Senha")

    # Campo para o usuário inserir o e-mail
    email = st.text_input("Digite seu e-mail:")

    # Botão para enviar e-mail de recuperação
    if st.button("Enviar e-mail de recuperação"):
        # Lógica para enviar e-mail com link de recuperação
        dados_email = {"email": email}
        response_forgot = requests.post(
            "http://localhost:5000/esqueceu_senha", json=dados_email
        )
        with st.spinner("Enviando email de recuperação..."):
            time.sleep(3)
        if response_forgot.status_code == 200:
            dados_rec = response_forgot.json()
            st.session_state.token = dados_rec["token_pass"]
            st.success(dados_rec["mensagem_pass"])
            st.toast("Redirecionando para a página de login.")
            time.sleep(3)
            st.switch_page("paginas/login.py")
        else:
            st.warning(
                f"Email não cadastrado. Código de resposta: {response_forgot.status_code}"
            )


exibir_pagina_esqueceu_senha()
