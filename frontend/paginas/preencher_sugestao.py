import streamlit as st
import pandas as pd
import datetime
import time, requests
from backend.tokens import pegar_id_com_token
from backend.banco_de_dados import Banco
from frontend.funcoes_paginas import criar_botoes_logouthome, sessao_expirada, nao_autorizado, preencher_documento, str_to_date
from frontend.controle_autenticacao import verificar_token, validar_token
from frontend.validacao import validar_acao, validar_justificativaobj, validar_sugestao, _contem_apenas_letras

def enviar_acoes_preenchidas_sugestao(acoes_preenchidas):
    try:
        response = requests.post("http://localhost:5000/enviar_sugestao", json=acoes_preenchidas)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao enviar sugestão preenchida: {str(e)}")

def exibir_pagina_formulario_sugestao():

    st.set_page_config(
        page_title="Formulário", page_icon="frontend/imagens/pref_icone.ico"
    )

    if verificar_token() and validar_token(st.session_state.get("token")):

        criar_botoes_logouthome()

        with st.form("my_form"):

            st.header(f"Formulário para sugestão de ação")

            cred_id = pegar_id_com_token(st.session_state.get("token") ) 
            informacoes = Banco().get_informacoes(cred_id)               
            info_id = Banco().get_info_id(cred_id)

            st.subheader("Dados da Secretaria/ Órgão Solicitante")
            
            responsavel_serv = informacoes[0][0]
            email_serv = informacoes[0][1]
            secretaria_serv = informacoes[0][2]
            telefone_serv = informacoes[0][4]
            cargo_serv = informacoes[0][6]
            
            st.write("Responsável pela Ação:", responsavel_serv)
            st.write("Cargo:", cargo_serv)
            st.write("Órgão/Secretaria:", secretaria_serv)
            st.write("Telefone:", telefone_serv)
            st.write("Email:", email_serv)

            st.subheader("Dados da ação")

            nome_acao = st.text_input("Ação: ")
            nom_acao = validar_acao(nome_acao)

            tipo_acao = st.radio(
                "Tipo de ação",
                [
                    "Curso",
                    "Webinário",
                    "Oficina",
                    "Seminário",
                    "Outros",
                ],
                index=None,
            )
            
            tip_acao = True if tipo_acao else False
            
            if tipo_acao == "Outros":
                tipo_acao = st.text_input(
                    "Fale qual seria o outro tipo de ação",
                    label_visibility="collapsed",
                )
                tip_acao = validar_acao(tipo_acao)
            
            num_vagas = st.number_input(
                "Número de vagas:",
                min_value=1,
                max_value=150,
                step=1,
            )
            
            carga_horaria = st.slider(
                "Sugestão de carga horária:",
                min_value=1,
                max_value=120,
                format="%d horas",
            )
            st.write(carga_horaria)

            # Obtendo a data de hoje
            today = datetime.datetime.now()
            jan_1 = datetime.date(today.year, 1, 1)
            dec_31 = datetime.date(today.year, 12, 31)

            # Obtendo a entrada de data do usuário
            periodo_str = st.text_input("Período da ação (Formato: DD/MM/AAAA)", f"{jan_1.strftime('%d/%m/%Y')} - {today.strftime('%d/%m/%Y')}")

            # Verificando se a entrada tem o formato esperado
            if len(periodo_str.split(" - ")) == 2:
                data_inicio_str, data_fim_str = periodo_str.split(" - ")
                
                # Verificando se as datas têm o formato esperado
                if len(data_inicio_str.split("/")) == 3 and len(data_fim_str.split("/")) == 3:
                    try:
                        data_inicio = str_to_date(data_inicio_str)
                        data_fim = str_to_date(data_fim_str)
                        # Mostrando as datas selecionadas
                        st.write("Data de início:", data_inicio)
                        st.write("Data de fim:", data_fim)
                    except ValueError:
                        st.error("Formato de data inválido. Por favor, insira as datas no formato DD/MM/AAAA.")
                else:
                    st.error("Formato de data inválido. Por favor, insira as datas no formato DD/MM/AAAA.")
            else:
                st.error("Formato de entrada inválido. Por favor, insira as datas no formato DD/MM/AAAA.")

            turno = st.selectbox(
                "Turno:",
                ["Matutino", "Vespertino"],
                index=None,
                placeholder="Turno...",
            )
            turn = True if turno else False

            modalidade = st.radio(
                "Modalidade",
                [
                    "Presencial",
                    "Semipresencial",
                    "Remoto até 2h por dia",
                    "EaD",
                ],
                index=None,
            )
            mod = True if modalidade else False
            
            publico = st.text_area("Público-alvo:")
            pub = True if validar_sugestao(publico) else False
            
            justificativa = st.text_area("Justificativa:")
            just = True if validar_sugestao(justificativa) else False
            
            objetivo = st.text_area("Objetivo:")
            obj = True if validar_sugestao(objetivo) else False
                        
            sugestao = st.text_area(
                "Sugestão de conteúdo programático:"
            )
            sug = True if validar_sugestao(sugestao) else False

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

            submitted = st.form_submit_button("Enviar formulário")
            if submitted:
                if all([nom_acao, tip_acao, turn, mod, pub, just, obj, sug]):
                    # Gravar a solicitação e obter o ID da solicitação recém-criada
                    sol_id = Banco().gravar_solicitacao(info_id, nome_acao, tipo_acao, num_vagas, carga_horaria, data_inicio, data_fim, turno, modalidade, publico, justificativa, objetivo, sugestao)
                    
                    if sol_id:  # Verificar se a solicitação foi gravada com sucesso
                        # Capturar os dados da tabela dos servidores
                        data_servidores = edited_df.to_dict('records')

                        # Ignora linhas completamente vazias
                        servidores_validos = []

                        for servidor in data_servidores:
                            preenchido = any(
                                pd.notna(valor) and str(valor).strip()
                                for valor in servidor.values()
                            )

                            if preenchido:
                                servidores_validos.append(servidor)

                        # Grava cada servidor e seu respectivo histórico
                        for servidor in servidores_validos:
                            nome = servidor.get('Nome')
                            matricula = servidor.get('Matrícula')
                            telefone = servidor.get('Telefone')
                            email = servidor.get('Email')

                            list_id = Banco().gravar_listagem(
                                nome, matricula, telefone, email, sol_id
                            )

                            if not list_id:
                                st.error("Erro ao registrar um dos servidores.")
                                break

                            Banco().gravar_historico_insercao(
                                list_id,
                                "Inserção da listagem de uma nova solicitação."
                            )
                        
                        # Converter a lista de servidores em um dicionário
                        dados_servidores_dict = {f"servidor_{i+1}": servidor for i, servidor in enumerate(data_servidores)}
                        
                        # Criar o dicionário dict_info e adicionar os dados dos servidores
                        dict_info = {
                            "servidores": dados_servidores_dict,
                            "responsavel": responsavel_serv,
                            "secretaria": secretaria_serv,
                            "cargo": cargo_serv,
                            "telefone": telefone_serv,
                            "email": email_serv,
                            "acao": nome_acao,
                            "tipo_acao": tipo_acao,
                            "num_vagas": num_vagas,
                            "carga_horaria": carga_horaria,
                            "data_inicio": data_inicio.strftime('%d/%m/%Y'),
                            "data_fim": data_fim.strftime('%d/%m/%Y'),
                            "turno": turno,
                            "publico_alvo": publico,
                            "modalidade": modalidade,
                            "justificativa": justificativa,
                            "obj": objetivo,
                            "sugestao_conteudo": sugestao
                        }
                        
                        response = enviar_acoes_preenchidas_sugestao(dict_info)
                                
                        # Tratar a resposta da API
                        if response and "mensagem" in response:
                            with st.spinner("Enviando formulário..."):
                                time.sleep(3)
                            st.success(response["mensagem"])    
                            st.toast("Redirecionando para o resumo.")
                            time.sleep(3)
                            st.switch_page("paginas/resumo.py")
                            st.rerun()
                        else:
                            st.error("Erro ao enviar sugestão. Por favor, tente novamente.")    
                        
                        #preencher_documento(dict_info)
                        
                        #st.success(
                        #    "Formulário de sugestão de ação preenchido com sucesso."
                        #)
                        #time.sleep(4)
                        #st.switch_page("paginas/resumo.py")
                    else:
                        st.error("Erro ao gravar a sugestão. Por favor, tente novamente.")
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios.")
            
    else:
        sessao_expirada() if verificar_token() else nao_autorizado()


exibir_pagina_formulario_sugestao()
