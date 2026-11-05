import streamlit as st
import time
import requests
from frontend.funcoes_paginas import (
    sessao_expirada,
    criar_botao_home,
    criar_botoes_logouthome,
    is_hexadecimal,
    pegar_orgaos,
    pegar_vinculos,
)
from frontend.validacao import (
    validar_senha,
    validar_nome,
    validar_usuario,
    validar_email,
    validar_CPF,
    validar_telefone,
    validar_secretaria,
    validar_acao,
    validar_matricula,
    validar_cargo,
    validar_vinculo,
    validar_campos_criacao
)
from frontend.controle_autenticacao import verificar_token, validar_token


def alterar_conta(dados_conta):
    try:
        response = requests.post(
            "http://localhost:5000/alterar_conta", json=dados_conta
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao alterar conta: {str(e)}")

def obter_dados(token_dict):
    try:
        response = requests.get("http://localhost:5000/dados", json = token_dict)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao obter dados do usuário da API: {str(e)}")
        
def exibir_pagina_alterar_dados():
        
    # Verifica se há um token de autenticação na sessão
    if verificar_token():
        # Verifica se o token é válido
        if validar_token(st.session_state.get("token")):
            
            token_dict = {"token" : (st.session_state.get("token"))}
            
            with st.spinner("Recebendo dados do servidor..."):
                dados = obter_dados(token_dict)
                
                if dados is None:
                    st.error("Não foi possível carregar os dados da conta. Verifique a API.")
                    st.stop()        
            # Se o token for válido, exibe os botões de home e logout
                       
            criar_botoes_logouthome()
            # Exibe o formulário para alterar dados
            st.title("Alterar dados")

            if st.toggle("Alterar senha"):
                senha = st.text_input("Senha:", type="password")
                sen = validar_senha(senha)
            else:
                senha = dados["senha"]
                sen = True

            tipo_senha = is_hexadecimal(senha)

            usuario = st.text_input("Usuário:", dados["usuario"])
            usu = validar_usuario(usuario)

            nome = st.text_input("Nome completo:", dados["nome"])
            nom = validar_nome(nome)

            email = st.text_input("E-mail:", dados["email"])
            em = validar_email(email)

            cpf = st.text_input("CPF:", dados["cpf"])
            cpff = validar_CPF(cpf)

            telefone = st.text_input(
                "Telefone (Preferência Whatsapp):", dados["telefone"]
            )
            tel = validar_telefone(telefone)

            secretaria = st.selectbox(
                "Orgão/Secretaria:",
                pegar_orgaos(),
                index=pegar_orgaos().index(dados["secretaria"]),
            )
            sec = validar_secretaria(secretaria)

            lotacao = st.text_input("Lotação:", dados["lotacao"])
            lot = validar_acao(lotacao)

            matricula = st.text_input("Matrícula:",dados["matricula"])
            mat = validar_matricula(matricula)

            cargo = st.text_input("Cargo:", dados["cargo"])
            carg = validar_cargo(cargo)

            col1, col2 = st.columns(2)
            with col1:
                vinculo = st.selectbox(
                    "Vínculo:",
                    pegar_vinculos(),
                    index=pegar_vinculos().index(dados["vinculo"]),
                )
            with col2:
                if vinculo == "Outro":
                    vinculo = st.text_input("")

            vinc = validar_vinculo(vinculo)

            value = st.checkbox(
                "Declaro para os devidos fins que POSSUO vínculo, direto ou indireto, com a Administração Pública Municipal de São Luís de acordo com as informações por mim registradas acima, ao mesmo tempo em que me responsabilizo pelo teor declarado. Com fulcro no Art. 299 (Código Penal), o qual tipifica o crime de Falsidade Ideológica."
            )
            
            check = (
                usu
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
                and sen
            )

            if st.button("Alterar dados"):
                if check and validar_campos_criacao(usuario, senha, nome, email, secretaria, cpf, telefone, matricula, cargo, vinculo, lotacao, value
                ):
                    dados_conta = {
                        "id": dados["id"],
                        "usuario": usuario,
                        "senha": senha,
                        "tipo_senha": tipo_senha,
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
                    response = alterar_conta(dados_conta)

                    # Tratar a resposta da API
                    if response and "mensagem" in response:
                        with st.spinner("Alterando dados..."):
                            time.sleep(3)
                        st.success(response["mensagem"])
                        st.toast("Redirecionando para o início.")
                        time.sleep(3)
                        st.switch_page("paginas/home.py")
                    else:
                        st.error("Erro ao alterar conta. Por favor, tente novamente.")
                else:
                    st.warning("Preencha todos os campos.")
        else:
            # Se o token não for válido, exibe mensagem de sessão expirada
            sessao_expirada()
    else:
        # Se não houver token na sessão, exibe apenas o botão de home e uma mensagem de acesso não autorizado
        criar_botao_home()
        st.error("Acesso não autorizado. Faça login para continuar.")
        
# Configuração da página
st.set_page_config(
        page_title="Alterar Dados", page_icon="frontend/imagens/pref_icone.ico"
    )

exibir_pagina_alterar_dados()
