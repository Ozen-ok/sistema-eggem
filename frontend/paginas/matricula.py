import streamlit as st
import pandas as pd
from backend.banco_de_dados import Banco
from frontend.funcoes_paginas import (
    criar_botoes_logouthome,
    sessao_expirada,
    adicionar_selecao,
    visualizar_curso,
    nao_autorizado,
)
from frontend.controle_autenticacao import verificar_token, validar_token

banco = Banco()


def exibir_pagina_selecao():

    st.set_page_config(
        page_title="Matrícula", page_icon="frontend/imagens/pref_icone.ico"
    )

    if not verificar_token():
        nao_autorizado()

    if not validar_token(st.session_state.get("token")):
        sessao_expirada()
        return

    if "tabela_cursos" not in st.session_state:
        st.session_state.tabela_cursos = pd.DataFrame(
            {"Ações selecionadas": [[], [], []]},
            index=[
                "FORMAÇÃO DE GESTORES, ESPECIALISTAS E CAPACITAÇÃO DO PESSOAL TÉCNICO - ADMINISTRATIVO",
                "FORMAÇÃO DIGITAL",
                "FORMAÇÃO EM LÍNGUA BRASILEIRA DE SINAIS",
            ],
        )

    criar_botoes_logouthome()
    st.title("Ações EGGEM")

    opcoes_comboboxes = [
        "FORMAÇÃO DE GESTORES, ESPECIALISTAS E CAPACITAÇÃO DO PESSOAL TÉCNICO - ADMINISTRATIVO",
        "FORMAÇÃO DIGITAL",
        "FORMAÇÃO EM LÍNGUA BRASILEIRA DE SINAIS",
    ]

    for i, opcao in enumerate(opcoes_comboboxes, start=1):
        opcoes_combobox = banco.pegar_cursos(opcao
        )
        selecao_combobox = st.selectbox(
            opcao + ":",
            opcoes_combobox,
            index=None,
            placeholder=f"Selecione uma ação para {opcao.lower()}",
        )
        if st.button(f"Adicionar ação ", key = i):
            if selecao_combobox:
                adicionar_selecao(
                    selecao_combobox, opcao, st.session_state.tabela_cursos
                )
            else:
                st.error(f"Nenhuma ação selecionada para {opcao.lower()}")

        if selecao_combobox:
            text = visualizar_curso(
                selecao_combobox, opcao
            )
            df = pd.DataFrame({"": text[0]}).set_index(
                pd.Index(["Ação", "Conteúdo Programático", "Carga horária"])
            )
            df.at["Conteúdo Programático", ""] = df.at["Conteúdo Programático", ""].replace(
                r"\n", "\n"
            )
            st.table(
                df.style.set_table_styles(
                    [{"selector": "thead", "props": "display: none;"}]
                )
            )

    dataframe_final = pd.DataFrame({"Ações selecionadas": []})

    for opcao in opcoes_comboboxes:
        if opcao in st.session_state.tabela_cursos.index \
                and st.session_state.tabela_cursos.at[opcao, "Ações selecionadas"]:
            dataframe = pd.DataFrame(
                {opcao: st.session_state.tabela_cursos.at[opcao, "Ações selecionadas"]}
            )
            dataframe_final = pd.concat(
                [
                    dataframe_final,
                    dataframe.rename(columns={dataframe.columns[0]: "Ações selecionadas"}),
                ],
                axis=0,
            )

    dataframe_final = dataframe_final.reset_index(drop=True)
    dataframe_final.index = range(1, len(dataframe_final) + 1)


    if not dataframe_final.empty:
        st.table(dataframe_final)

    if st.button("Limpar ações"):
        st.session_state.tabela_cursos = pd.DataFrame(
            {"Ações selecionadas": [[], [], []]},
            index=[
                "FORMAÇÃO DE GESTORES, ESPECIALISTAS E CAPACITAÇÃO DO PESSOAL TÉCNICO - ADMINISTRATIVO",
                "FORMAÇÃO DIGITAL",
                "FORMAÇÃO EM LÍNGUA BRASILEIRA DE SINAIS",
            ],
        )
        st.rerun()

    if st.button("Preencher formulário"):
        if not dataframe_final.empty:
            st.session_state.df = dataframe_final
            st.switch_page("paginas/preencher_formulario.py")
        else:
            st.warning("Adicione alguma ação antes de preencher o formulário.")
            
    if st.button("Deseja sugerir uma ação?"):
            st.switch_page("paginas/preencher_sugestao.py")

exibir_pagina_selecao()
