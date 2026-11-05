import streamlit as st
from backend.tokens import verificar_exp_token


def verificar_token():
    """
    Verifica se há um token na sessão do Streamlit.
    """
    return st.session_state.get("token") is not None


def validar_token(token):
    """
    Valida o token verificando sua autenticidade e validade.
    """
    if token:
        if verificar_exp_token(token):
            # Aqui você pode adicionar outras verificações, como validar se o token é associado ao usuário atual
            return True
    return False
