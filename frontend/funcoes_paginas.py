import time
import pandas as pd
import streamlit as st
import datetime
from docxtpl import DocxTemplate
from docx import Document
from io import BytesIO
import base64

def criar_botao_logout():
    if st.button("logout", key="logout"):
        with st.spinner("Saindo da conta..."):
            time.sleep(3)
        st.success("Logout realizado com sucesso!")
        st.toast("Redirecionando para o início.")
        time.sleep(3)
        st.session_state.token = None
        st.session_state.authenticated = False
        st.session_state.tabela_cursos = pd.DataFrame(
            {"Cursos selecionados": [[], [], []]}
        ).set_index(
            pd.Index(
                [
                    "FORMAÇÃO DE GESTORES, ESPECIALISTAS E CAPACITAÇÃO DO PESSOAL TÉCNICO - ADMINISTRATIVO",
                    "FORMAÇÃO DIGITAL",
                    "FORMAÇÃO EM LÍNGUA BRASILEIRA DE SINAIS",
                ]
            )
        )
        st.session_state.df = None
        st.switch_page("paginas/home.py")


def criar_botao_home():
    if st.button("Home ", key="home"):
        st.switch_page("paginas/home.py")


def criar_botoes_logouthome():
    col1, col2 = st.columns([0.5, 0.047])
    if col1.button("Home ", key="home"):
        st.switch_page("paginas/home.py")

    if col2.button("Sair", key="logout"):
        with st.spinner("Saindo da conta..."):
            time.sleep(3)
        st.success("Logout realizado com sucesso!")
        st.toast("Redirecionando para o início.")
        time.sleep(3)
        st.session_state.token = None
        st.session_state.authenticated = False
        st.session_state.tabela_cursos = pd.DataFrame(
            {"Cursos selecionados": [[], [], []]}
        ).set_index(
            pd.Index(
                [
                    "FORMAÇÃO DE GESTORES, ESPECIALISTAS E CAPACITAÇÃO DO PESSOAL TÉCNICO - ADMINISTRATIVO",
                    "FORMAÇÃO DIGITAL",
                    "FORMAÇÃO EM LÍNGUA BRASILEIRA DE SINAIS",
                ]
            )
        )
        st.session_state.df = None
        st.switch_page("paginas/home.py")


def sessao_expirada():
    st.error("Sessão expirada. Faça login novamente para continuar.")
    time.sleep(5)
    st.session_state.token = None
    st.session_state.authenticated = False
    st.session_state.df = None
    st.session_state.tabela_cursos = pd.DataFrame(
        {"Cursos selecionados": [[], [], []]}
    ).set_index(
        pd.Index(
            [
                "FORMAÇÃO DE GESTORES, ESPECIALISTAS E CAPACITAÇÃO DO PESSOAL TÉCNICO - ADMINISTRATIVO",
                "FORMAÇÃO DIGITAL",
                "FORMAÇÃO EM LÍNGUA BRASILEIRA DE SINAIS",
            ]
        )
    )
    st.switch_page("paginas/login.py")


def nao_autorizado():
    st.error("Acesso não autorizado. Faça login para continuar.")
    time.sleep(5)
    st.switch_page("paginas/login.py")


def is_hexadecimal(senha):
    return senha.startswith("\\x") and all(
        c in "0123456789abcdefABCDEF" for c in senha[2:]
    )


def adicionar_selecao(selecao, tabela_str, selecoes):

    # Adiciona a seleção à lista se ainda não estiver presente
    if selecao not in selecoes.at[tabela_str, "Ações selecionadas"]:
        cursos_selecionados = selecoes.at[tabela_str, "Ações selecionadas"]
        cursos_selecionados.append(selecao)

        selecoes.at[tabela_str, "Ações selecionadas"] = cursos_selecionados
        st.success("Ação adicionada com sucesso.")
    else:
        st.warning("Ação já adicionado.")


def visualizar_curso(curso, table=None):
    from backend.banco_de_dados import Banco

    curso_texto = Banco().buscar_curso(curso)
    return curso_texto


def pegar_orgaos():
    return [
        "SADEM",
        "SECOM",
        "SECULT",
        "SEMAD",
        "SEMAI",
        "SEMAP",
        "SEMAPA",
        "SEMCAS",
        "SEMDEL",
        "SEMED",
        "SEMFAZ",
        "SEMGOP",
        "SEMGOV",
        "SEMIT",
        "SEMMAM",
        "SEMEPED",
        "SEMOSP",
        "SEMISPE",
        "SEMSA",
        "SEMURH",
        "SEMUSC",
        "SEMUS",
        "SEPLAN",
        "SETUR",
        "SMTT",
        "AMDES",
        "Coordenadoria da Mulher",
        "CGLU",
        "CGM",
        "CPL",
        "FUMPH",
        "GAVIC",
        "IMPUR",
        "INCID",
        "IPAM",
        "PGM",
        "SOCORRÃO 1",
        "SOCORRÃO 2",
    ]


def pegar_vinculos():
    return [
        "Efetivo",
        "Comissionado",
        "Serviço Prestado",
        "Contrato Temporário",
        "Celetista/CLT",
        "Outro",
    ]

# Função para converter string de data para objeto de data
def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, '%d/%m/%Y').date()

def teste(dados):
    dados_sec = {
        "nome": "João da Silva",
        "email": "testemail@gmail.com",
        "orgao": "SEMED",
        "telefone": "9892849849",
        "acao": "Ação teste teste",
        "tipo_acao": "Webinário",
        "num_vagas": "30",
        "sugestao_carga": "40",
        "periodo": "26/04/2024 a 30/04/2024",
        "turno": "Matutino",
        "modalidade": "Semipresencial",
        "justificativa": "balbaolabala",
        "obj": "testar o programa",
        "sugestao_conteudo": "capitulo 1 capitulo 2 etc"
    }
    import streamlit as st
    
    st.write(dados)
    
    caminho_modelo = "frontend/formulario_modelo.docx"

    # Carregar o modelo
    doc = DocxTemplate(caminho_modelo)

    # Preencher o modelo com as informações
    doc.render(dados)

    # Salvar o documento preenchido
    caminho_documento_preenchido = "frontend/documento_preenchido.docx"
    doc.save(caminho_documento_preenchido)

def preencher_tabela(doc, dados_servidores):
    # Encontra a segunda tabela no documento
    for tabela in doc.tables:
        # Verifica se a tabela tem pelo menos uma linha
        if len(tabela.rows) > 0:
            # Verifica se a primeira célula da primeira linha contém "NOME"
            if tabela.rows[0].cells[0].text.strip().upper() == "NOME":
                # Loop sobre os servidores e preenche cada linha da tabela
                for chave_servidor, servidor in dados_servidores.items():
                    row = tabela.add_row().cells
                    row[0].text = servidor.get("Nome", "")
                    row[1].text = servidor.get("Matrícula", "")
                    row[2].text = servidor.get("Telefone", "")
                    row[3].text = servidor.get("Email", "")
                break  # Para de procurar mais tabelas depois de encontrar e preencher a primeira que atende aos critérios



def preencher_documento(dados, tipo_doc):
    
    caminho_modelo="frontend/formulario_modelo.docx"
    
    if tipo_doc == "solicitacao":
        # Tipo 1: Solicitação de ação
        gerar_solicitacao(dados, caminho_modelo)
    elif tipo_doc == "sugestao":
        # Tipo 2: Sugestão de ação
        gerar_sugestao(dados, caminho_modelo)
    else:
        # Tipo inválido
        return False

import docx2pdf

def gerar_solicitacao(dados, caminho_modelo, pasta_destino):
    documentos_gerados = []
    num_arquivo = 1  # Inicializa o número do arquivo
    
    for num_arquivo, acao in enumerate(dados, start=1):
        ano_atual = datetime.datetime.now().year
        sec = acao.get("secretaria")
        caminho_documento_preenchido_docx = f"{pasta_destino}/Solicitacao {num_arquivo} - D.E - {sec} - {ano_atual}.docx"
        caminho_documento_preenchido_pdf = f"{pasta_destino}/Solicitacao {num_arquivo} - D.E - {sec} - {ano_atual}.pdf"

        doc = Document(caminho_modelo)
        dados_servidores = acao.get("servidores", [])
        preencher_tabela(doc, dados_servidores)
        doc.save(caminho_documento_preenchido_docx)
        doc_tpl = DocxTemplate(caminho_documento_preenchido_docx)

        dados_sec = {
            "responsavel": acao.get("responsavel", ""),
            "secretaria": acao.get("secretaria", ""),
            "cargo": acao.get("cargo", ""),
            "telefone": acao.get("telefone", ""),
            "email": acao.get("email", ""),
            "acao": acao.get("acao", ""),
            "tipo_acao": acao.get("tipo_acao", ""),
            "num_vagas": acao.get("num_vagas", ""),
            "carga_horaria": acao.get("carga_horaria", ""),
            "data_inicio": acao.get("data_inicio", ""),
            "data_fim": acao.get("data_fim", ""),
            "turno": acao.get("turno", ""),
            "publico_alvo": acao.get("publico_alvo", ""),
            "modalidade": acao.get("modalidade", ""),
            "justificativa": acao.get("justificativa", ""),
            "obj": acao.get("objetivo", ""),
            "sugestao_conteudo": acao.get("sugestao_conteudo", "")
        }

        doc_tpl.render(dados_sec)
        doc_tpl.save(caminho_documento_preenchido_docx)
        
        # Convertendo para PDF
        docx2pdf.convert(caminho_documento_preenchido_docx, caminho_documento_preenchido_pdf)
        
        documentos_gerados.append({"caminho": caminho_documento_preenchido_pdf, "secretaria": sec, "ano_atual": ano_atual})
    
    return documentos_gerados


def gerar_sugestao(dados, caminho_modelo, pasta_destino):
    
    documentos_gerados = []
  
    ano_atual = datetime.datetime.now().year
    sec = dados.get("secretaria")
    caminho_documento_preenchido_docx = f"{pasta_destino}/Sugestao - D.E - {sec} - {ano_atual}.docx"
    caminho_documento_preenchido_pdf = f"{pasta_destino}/Sugestao - D.E - {sec} - {ano_atual}.pdf"

    # Carrega o modelo do documento
    doc = Document(caminho_modelo)

    # Adiciona dados dos servidores à tabela
    dados_servidores = dados.get("servidores", [])
    preencher_tabela(doc, dados_servidores)

    # Salva o documento com a tabela preenchida
    doc.save(caminho_documento_preenchido_docx)

    # Carrega o documento preenchido como template do docxtpl
    doc_tpl = DocxTemplate(caminho_documento_preenchido_docx)

    # Adiciona outros dados ao modelo
    dados_sec = {
        "responsavel": dados.get("responsavel", ""),
        "secretaria": dados.get("secretaria", ""),
        "cargo": dados.get("cargo", ""),
        "telefone": dados.get("telefone", ""),
        "email": dados.get("email", ""),
        "acao": dados.get("acao", ""),
        "tipo_acao": dados.get("tipo_acao", ""),
        "num_vagas": dados.get("num_vagas", ""),
        "carga_horaria": dados.get("carga_horaria", ""),
        "data_inicio": dados.get("data_inicio", ""),
        "data_fim": dados.get("data_fim", ""),
        "turno": dados.get("turno", ""),
        "publico_alvo": dados.get("publico_alvo", ""),
        "modalidade": dados.get("modalidade", ""),
        "justificativa": dados.get("justificativa", ""),
        "obj": dados.get("objetivo", ""),
        "sugestao_conteudo": dados.get("sugestao_conteudo", "")
    }

    # Renderiza os dados no modelo
    doc_tpl.render(dados_sec)

    # Salva o documento preenchido
    doc_tpl.save(caminho_documento_preenchido_docx)
    
    # Convertendo para PDF
    docx2pdf.convert(caminho_documento_preenchido_docx, caminho_documento_preenchido_pdf)
    
    documentos_gerados.append({"caminho": caminho_documento_preenchido_pdf, "secretaria": sec, "ano_atual": ano_atual})
    
    return documentos_gerados

def get_download_link(conteudo, nome_arquivo):
    # Codificar o conteúdo do arquivo para base64
    conteudo_base64 = base64.b64encode(conteudo).decode()

    # Criar o link de download
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{conteudo_base64}" download="{nome_arquivo}">Clique aqui para baixar</a>'
    return href

#from docx import Document

def imprimir_tabelas(documento):
    """
    Função para imprimir todas as tabelas encontradas em um documento.
    """
    for i, tabela in enumerate(documento.tables, start=1):
        print(f"Tabela {i}:")
        for row in tabela.rows:
            for cell in row.cells:
                print(cell.text)
            print()  # Adiciona uma linha em branco após cada linha da tabela
        print("=" * 20)  # Adiciona uma linha divisória entre tabelas

## Carregue o documento
#caminho_documento = "frontend/formulario_modelo.docx"
#documento = Document(caminho_documento)

# Imprima todas as tabelas no documento
#imprimir_tabelas(documento)
