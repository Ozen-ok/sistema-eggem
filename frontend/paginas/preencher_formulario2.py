import streamlit as st
import pandas as pd
import datetime
import time
from backend.tokens import pegar_id_com_token
from backend.banco_de_dados import Banco
from frontend.funcoes_paginas import (
    criar_botoes_logouthome,
    sessao_expirada,
    nao_autorizado,
)
from frontend.controle_autenticacao import verificar_token, validar_token


def exibir_pagina_formulario():

    st.set_page_config(
        page_title="Formulário", page_icon="frontend/imagens/pref_icone.ico"
    )

    if verificar_token() and validar_token(st.session_state.get("token")):

        criar_botoes_logouthome()

        if "df" in st.session_state:

            st.write(st.session_state.df)

            st.session_state.index_selecionado = st.session_state.get(
                "index_selecionado", 0
            )

            if st.button("Resetar index"):
                st.session_state.index_selecionado = 0
                st.rerun()
            if st.button("Ir até página resumo"):
                st.success("Formulário de solicitação de ação preenchido com sucesso.")
                time.sleep(4)
                st.switch_page("paginas/resumo.py")

            cursos_selecionados = st.session_state.df["Ações selecionadas"].tolist()

            curso_atual = cursos_selecionados[st.session_state.index_selecionado]

            with st.form("my_form"):

                st.header(f"Formulário para solicitação de ação - {curso_atual}")

                cred_id = pegar_id_com_token(st.session_state.get("token") ) 
                informacoes = Banco().get_informacoes(cred_id)

                st.subheader("Dados da Secretaria/ Órgão Solicitante")
                
                info_id = Banco().get_info_id(cred_id)

                nome = st.write("Nome:", informacoes[0][0])
                email = st.write("Email:", informacoes[0][1])
                orgao = st.write("Órgão/Secretaria:", informacoes[0][2])
                telefone = st.write("Telefone:", informacoes[0][4])

                st.subheader("Dados da ação")

                nome_acao = st.write("Ação: ", curso_atual)

                tipo_acao = st.radio(
                    "Tipo de ação",
                    [
                        "Curso",
                        "Webinário",
                        "Oficina",
                        "Seminário :movie_camera:",
                        "Outros",
                    ],
                    index=None,
                )

                if tipo_acao == "Outros":
                    tipo_acao = st.text_input(
                        "Fale qual seria o outro tipo de ação",
                        label_visibility="collapsed",
                    )

                col1, col2, col3, col4 = st.columns(4)

                num_vagas = col1.text_input("Número de vagas:")
                carga_horaria = col2.text_input(
                    "Sugestão de carga horária:",
                    Banco().buscar_curso(curso_atual)[0][2],
                )

                today = datetime.datetime.now()
                jan_1 = datetime.date(today.year, 1, 1)
                dec_31 = datetime.date(today.year, 12, 31)

                periodo = col3.date_input(
                    "Período da ação",
                    (jan_1, datetime.date(today.year, 1, 7)),
                    jan_1,
                    dec_31,
                    format="YYYY-MM-DD",
                )

                data_inicio = periodo[0]
                data_fim = periodo[1]

                turno = col4.selectbox(
                    "Turno:",
                    ["Matutino", "Vespertino"],
                    index=None,
                    placeholder="Turno...",
                )

                modalidade = st.radio(
                    "Modalidade",
                    [
                        "Presencial",
                        "Semipresencial",
                        "Remoto até 2h por dia :movie_camera:",
                        "EaD",
                    ],
                    index=None,
                )
                justificativa = st.text_area("Justificativa:")
                objetivo = st.text_area("Objetivo:")
                sugestao = st.text_area(
                    "Sugestão de conteúdo programático:",
                    Banco().buscar_curso(curso_atual)[0][1],
                )

                st.subheader("Listagem dos servidores")

                df = pd.DataFrame(
                    [
                        {"Nome": "", "Matrícula": "", "Telefone": "", "Email": ""},
                    ]
                )

                edited_df = st.data_editor(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    num_rows=("dynamic"),
                )

                submitted = st.form_submit_button("Próximo curso")
                if submitted:
                    Banco.gravar_solicitacao(info_id, nome_acao, tipo_acao, num_vagas, carga_horaria, data_inicio, data_fim, turno, modalidade, justificativa, objetivo, sugestao)
                    st.session_state.index_selecionado += 1
                    if st.session_state.index_selecionado >= len(cursos_selecionados):
                        st.success(
                            "Formulário de solicitação de ação preenchido com sucesso."
                        )
                        time.sleep(4)
                        st.session_state.index_selecionado = 0
                        st.switch_page("paginas/resumo.py")
                    st.rerun()

        else:
            st.warning("Selecione as ações desejadas antes de preencher o formulário.")
    else:
        sessao_expirada() if verificar_token() else nao_autorizado()


exibir_pagina_formulario()
