-- Banco de desenvolvimento/teste do Sistema EGGEM.
-- Execute este arquivo dentro de um banco já criado (ex.: sistema_eggem_dev).
-- O script cria as tabelas ausentes e insere cursos fictícios de exemplo.
-- Ele NÃO atualiza tabelas existentes; use uma migração específica se o schema mudar.
-- Faça backup antes de executar em um banco que já contenha dados.

BEGIN;

CREATE TABLE IF NOT EXISTS credenciais (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL UNIQUE,
    senha BYTEA NOT NULL
);

CREATE TABLE IF NOT EXISTS informacoes_usuario (
    id SERIAL PRIMARY KEY,
    cred_id INTEGER NOT NULL REFERENCES credenciais(id),
    nome VARCHAR(255),
    email VARCHAR(255),
    secretaria VARCHAR(255),
    cpf VARCHAR(20),
    celular VARCHAR(30),
    matricula VARCHAR(50),
    cargo_funcao VARCHAR(255),
    vinculo VARCHAR(255),
    lotacao VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS formacao_gestao (
    id SERIAL PRIMARY KEY,
    curso VARCHAR,
    sugestao_conteudo VARCHAR,
    carga_horaria VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS formacao_digital (
    id SERIAL PRIMARY KEY,
    curso VARCHAR,
    sugestao_conteudo VARCHAR,
    carga_horaria VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS formacao_linguas (
    id SERIAL PRIMARY KEY,
    curso VARCHAR,
    sugestao_conteudo VARCHAR,
    carga_horaria VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS formulario_solicitacao (
    id SERIAL PRIMARY KEY,
    formulario_id INTEGER NOT NULL REFERENCES informacoes_usuario(id),
    nome_acao VARCHAR(255),
    tipo_acao VARCHAR(100),
    num_vagas INTEGER,
    carga_horaria INTEGER,
    data_inicio DATE,
    data_fim DATE,
    turno VARCHAR(100),
    modalidade VARCHAR(100),
    publico_alvo TEXT,
    justificativa TEXT,
    objetivo TEXT,
    sugestao TEXT
);

CREATE TABLE IF NOT EXISTS listagem_servidores (
    id SERIAL PRIMARY KEY,
    solicitacao_id INTEGER NOT NULL REFERENCES formulario_solicitacao(id),
    nome VARCHAR(255),
    matricula VARCHAR(50),
    telefone VARCHAR(30),
    email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS historico_alteracoes_servidores (
    id SERIAL PRIMARY KEY,
    listagem_servidores_id INTEGER NOT NULL
        REFERENCES listagem_servidores(id),
    data_hora TIMESTAMP,
    tipo_alteracao VARCHAR(100),
    detalhes TEXT
);

-- Quatro cursos ficticios para validar a consulta e a selecao no frontend.
INSERT INTO formacao_gestao (curso, sugestao_conteudo, carga_horaria)
SELECT dados.curso, dados.sugestao_conteudo, dados.carga_horaria
FROM (VALUES
    ('Comunicacao Assertiva no Servico Publico',
     'Comunicacao interpessoal; escuta ativa; resolucao de conflitos; comunicacao nao violenta.',
     '24 horas'),
    ('Gestao de Pessoas e Lideranca',
     'Lideranca no setor publico; gestao de equipes; motivacao; desenvolvimento profissional.',
     '20 horas'),
    ('Planejamento Estrategico Governamental',
     'Planejamento estrategico; definicao de metas; indicadores de desempenho; gestao de resultados.',
     '16 horas'),
    ('Excel Aplicado a Administracao Publica',
     'Planilhas; formulas; funcoes; tabelas dinamicas; organizacao e analise de dados.',
     '12 horas')
) AS dados(curso, sugestao_conteudo, carga_horaria)
WHERE NOT EXISTS (
    SELECT 1 FROM formacao_gestao existente
    WHERE existente.curso = dados.curso
);

COMMIT;

-- Conferencia:
-- SELECT * FROM formacao_gestao ORDER BY id;
-- SELECT table_name FROM information_schema.tables
-- WHERE table_schema = 'public' ORDER BY table_name;
