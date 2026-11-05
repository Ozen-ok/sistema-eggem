import streamlit as st
from docx import Document


def exibir_resumo_formulario():

    st.set_page_config(page_title="Resumo", page_icon="frontend/imagens/pref_icone.ico")

    def ler_docx(caminho_arquivo):
        doc = Document("frontend\documento_preenchido.docx")
        texto = ""
        for paragrafo in doc.paragraphs:
            texto += paragrafo.text + "\n"
        return texto

    
    #st.title("Visualizador de Arquivo DOC")
    caminho_arquivo = st.file_uploader("Carregar arquivo DOC", type=["docx"])
    if caminho_arquivo is not None:
        conteudo = ler_docx(caminho_arquivo)
        st.text_area("Conteúdo do Arquivo DOC", value=conteudo, height=600)


exibir_resumo_formulario()
