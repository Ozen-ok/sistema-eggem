from st_pages import Page, Section, show_pages
import streamlit as st

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("frontend/paginas/home.py", "Home", "🏫"),
        Section(name="Conta", icon="🎈️"),
        Page("frontend/paginas/criar_conta.py", "Criar conta", "🆕"),
        Page("frontend/paginas/esqueceu_a_senha.py", "Esqueceu a senha", "🔑"),
        Page("frontend/paginas/login.py", "Login", "⛷️"),
        Page("frontend/paginas/alterar_dados.py", "Alterar Dados", "🔧"),
        Section(name="Ações", icon="📅"),
        Page("frontend/paginas/matricula.py", "Matrícula", "📚"),
        Page("frontend/paginas/preencher_formulario.py", "Formulário", "📃"),
        Page("frontend/paginas/preencher_sugestao.py", "Sugestão", "📃"),
        Page("frontend/paginas/resumo.py", "Resumo do formulário", "📃"),
    ]
)

st.switch_page("paginas/home.py")
