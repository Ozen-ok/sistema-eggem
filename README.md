# Sistema de Gestão de Ações de Capacitação — EGGEM

Aplicação desenvolvida durante um estágio na Escola de Governo e Gestão Municipal (EGGEM), com o propósito de apoiar o fluxo de ações de capacitação: autenticação de usuários, consulta de cursos, preenchimento de solicitações e sugestões, geração de documentos e envio por e-mail.

> **Contexto:** este repositório registra uma versão histórica do projeto, desenvolvida durante o período de estágio. Não representa necessariamente os procedimentos ou contatos institucionais atualmente vigentes e não deve ser tratado como um sistema pronto para produção.

## Tecnologias

- **Python** — linguagem principal
- **FastAPI** — API
- **Streamlit** — interface web
- **PostgreSQL** — banco de dados
- **bcrypt e JWT** — recursos de autenticação
- **python-docx e docxtpl** — geração de documentos
- **FastAPI-Mail** — envio de e-mails

## Estrutura do projeto

```text
sistema-eggem/
├── backend/
│   ├── api1.py
│   ├── banco_de_dados.py
│   ├── tokens.py
│   └── formulario_modelo.docx
├── frontend/
│   ├── paginas/
│   ├── imagens/
│   ├── st_app.py
│   ├── funcoes_paginas.py
│   ├── controle_autenticacao.py
│   └── validacao.py
├── tests/
│   └── teste_gerardoc.py
├── .env.example
├── .gitignore
├── egg_em_banco_teste.sql
├── main.py
├── run_streamlit.py
└── requirements.txt
```

O modelo `backend/formulario_modelo.docx` é a referência utilizada pela API para gerar as solicitações. Os documentos institucionais foram preservados como registros históricos da época do desenvolvimento.

## Requisitos

- Python 3.11
- PostgreSQL
- Windows é recomendado para a conversão DOCX → PDF com `docx2pdf`, pois esse fluxo depende do Microsoft Word instalado.

## Configuração

Execute os comandos a partir da pasta raiz `sistema-eggem/`.

### 1. Criar e ativar um ambiente virtual

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows (Prompt de Comando):

```bat
python -m venv .venv
.venv\Scripts\activate
```

### 2. Instalar as dependências

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

Copie `.env.example` para `.env` e preencha os valores locais:

```powershell
Copy-Item .env.example .env
```

Configure os dados de conexão do PostgreSQL, uma `SECRET_KEY` aleatória e as credenciais SMTP. Não compartilhe nem versione o arquivo `.env`.

### 4. Criar e preparar o banco de dados

Crie primeiro um banco PostgreSQL vazio, por exemplo `sistema_eggem_dev`, com um usuário que tenha permissão para criar tabelas.

Depois execute o script SQL `egg_em_banco_teste.sql` nesse banco. Ele cria as tabelas utilizadas pelo projeto e insere quatro cursos fictícios de exemplo em `formacao_gestao`.

O script é destinado a um banco de desenvolvimento/teste. Faça backup antes de executá-lo em qualquer banco que já contenha dados. O script usa `CREATE TABLE IF NOT EXISTS`, mas não é uma ferramenta de migração para atualizar estruturas antigas.

Exemplo usando `psql`:

```bash
psql -U postgres -d sistema_eggem_dev -f egg_em_banco_teste.sql
```

### 5. Iniciar a aplicação

Abra dois terminais na raiz do projeto.

**Terminal 1 — API:**

```bash
python main.py
```

A API inicia em `http://localhost:5000`. A documentação interativa do FastAPI fica em `http://localhost:5000/docs`.

**Terminal 2 — interface Streamlit:**

```bash
python run_streamlit.py
```

A interface inicia em `http://localhost:5001`.

## Teste manual de geração de documento

O script `tests/teste_gerardoc.py` é independente da inicialização normal do sistema. Ele usa o mesmo modelo DOCX da API, preenche dados fictícios e grava o resultado em `tests/saidas/`.

Execute na raiz:

```bash
python tests/teste_gerardoc.py
```

O teste não envia e-mails nem grava informações no banco de dados.

## Observações importantes

- O `.env` contém segredos e credenciais locais; nunca deve ser enviado ao Git.
- Os dados usados no teste de geração de documentos são fictícios.
- O modelo DOCX e as instruções institucionais foram mantidos no contexto histórico do projeto. Confirme sua validade com a instituição antes de reutilizá-los operacionalmente.
- O envio de e-mails depende de uma conta SMTP configurada corretamente.
- A conversão de documentos para PDF com `docx2pdf` depende de ambiente Windows com Microsoft Word instalado.
- Antes de qualquer implantação pública ou produtiva, o código precisa de revisão adicional de segurança, autenticação/autorização, configuração de CORS, tratamento de erros, testes automatizados e atualização das dependências.

## Licença e uso

Nenhuma licença de distribuição foi declarada neste repositório. Antes de redistribuir o código, imagens ou modelos institucionais, confirme os direitos de uso aplicáveis.
