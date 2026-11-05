import streamlit as st, time, requests
from fastapi import HTTPException
from frontend.validacao import (
    validar_senha,
    validar_nome,
    validar_usuario,
    validar_email,
    validar_CPF,
    validar_telefone,
    validar_secretaria,
    validar_matricula,
    validar_cargo,
    validar_vinculo,
    validar_campos_criacao,
    validar_campos_login,
    validar_acao
)
from frontend.funcoes_paginas import criar_botao_home, pegar_orgaos, pegar_vinculos


def criar_conta(dados_conta):
    try:
        response = requests.post("http://localhost:5000/criar_conta", json=dados_conta)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_error:
        status_code = http_error.response.status_code
        if status_code == 409:
            st.error("Erro ao criar conta: Usuário ou senha já existem.")
        elif status_code == 500:
            st.error("Erro ao criar conta: Erro interno do servidor.")
        else:
            st.error(f"Erro ao criar conta: {status_code}")
    except Exception as e:
        st.error(f"Erro ao criar conta: não foi possível se conectar ao servidor.")


def exibir_pagina_criar_conta():

    st.set_page_config(
        page_title="Criar conta", page_icon="frontend/imagens/pref_icone.ico"
    )

    criar_botao_home()

    st.title("Cadastrar uma conta")

    novo_usuario = st.text_input(
        "Novo Usuário:", placeholder="Apenas letras minúsculas e números, sem acentos."
    )
    user = validar_usuario(novo_usuario)

    nova_senha = st.text_input(
        "Nova Senha:",
        placeholder="Uma letra maiúscula, uma letra minúscula, um número e ao menos 8 caracteres.",
        type="password",
    )
    passw = validar_senha(nova_senha)

    confirmar_senha = st.text_input(
        "Confirme a senha:", placeholder="Repita a senha.", type="password"
    )

    if confirmar_senha and nova_senha != confirmar_senha:
        st.warning("As senhas não coincidem!")

    nome = st.text_input("Nome completo:")
    nom = validar_nome(nome)

    email = st.text_input("E-mail:")
    em = validar_email(email)

    cpf = st.text_input("CPF:")
    cpff = validar_CPF(cpf)

    telefone = st.text_input(
        "Telefone (Preferência Whatsapp):", placeholder="Formato: DDD + 9XXXXXXXX"
    )
    tel = validar_telefone(telefone)

    secretaria_opcoes = pegar_orgaos()
    secretaria = st.selectbox(
        "Orgão/Secretaria:",
        secretaria_opcoes,
        index=None,
        placeholder="Selecione um orgão/secretaria...",
    )
    sec = validar_secretaria(secretaria)

    lotacao = st.text_input("Lotação:")
    lot = validar_acao(lotacao)

    matricula = st.text_input("Matrícula:", placeholder="Apenas números.")
    mat = validar_matricula(matricula)

    cargo = st.text_input("Cargo:")
    carg = validar_cargo(cargo)

    col1, col2 = st.columns(2)
    with col1:
        vinculo = st.selectbox(
            "Vínculo:",
            pegar_vinculos(),
            index=None,
            placeholder="Selecione um vínculo...",
        )
    with col2:
        if vinculo == "Outro":
            vinculo = st.text_input("")

    vinc = validar_vinculo(vinculo)

    value = st.checkbox(
        "Declaro para os devidos fins que POSSUO vínculo, direto ou indireto, com a Administração Pública Municipal de São Luís de acordo com as informações por mim registradas acima, ao mesmo tempo em que me responsabilizo pelo teor declarado. Com fulcro no Art. 299 (Código Penal), o qual tipifica o crime de Falsidade Ideológica."
    )
    check = (
        user
        and passw
        and nom
        and em
        and sec
        and cpff
        and tel
        and mat
        and carg
        and vinc
        and lot
        and value
    )

    if st.button("Criar Conta"):
        if (
            validar_campos_criacao(
                novo_usuario,
                nova_senha,
                nome,
                email,
                secretaria,
                cpf,
                telefone,
                matricula,
                cargo,
                vinculo,
                lotacao,
                value                
            )
            and check
            and nova_senha == confirmar_senha
            and validar_campos_login(novo_usuario, nova_senha)
        ):
            dados_conta = {
                "novo_usuario": novo_usuario,
                "nova_senha": nova_senha,
                "nome": nome,
                "email": email,
                "cpf": cpf,
                "telefone": telefone,
                "secretaria": secretaria,
                "lotacao": lotacao,
                "matricula": matricula,
                "cargo": cargo,
                "vinculo": vinculo,
            }

            # Chamar a função para criar a conta na API FastAPI
            response = criar_conta(dados_conta)

            # Tratar a resposta da API
            if response and "mensagem" in response:
                with st.spinner("Criando conta..."):
                    time.sleep(3)
                st.success(response["mensagem"])
                st.toast("Redirecionando para página de login.")
                time.sleep(3)
                st.switch_page("paginas/login.py")

exibir_pagina_criar_conta()
