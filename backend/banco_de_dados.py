import json
import os
from dotenv import load_dotenv

load_dotenv()
import psycopg2
import bcrypt
import datetime
from frontend.validacao import _contem_caracteres_especiais

class Banco:
    def __init__(self):
        # Configuração do banco de dados
        self.config = {
            'dbname': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
        }
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Abre a conexão no início do bloco with
        self.conn = psycopg2.connect(**self.config)
        self.cursor = self.conn.cursor()
        return self  # Retorna a instância da classe para uso no bloco with

    def __exit__(self, exc_type, exc_value, traceback):
        # Fecha a conexão no final do bloco with
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()
            
    def get_table(self, table):
               
        if table == "FORMAÇÃO DE GESTORES, ESPECIALISTAS E CAPACITAÇÃO DO PESSOAL TÉCNICO - ADMINISTRATIVO":
            return "SELECT curso, sugestao_conteudo, carga_horaria FROM formacao_gestao WHERE curso = %s;"
        elif table == "FORMAÇÃO DIGITAL":
            return "SELECT curso, sugestao_conteudo, carga_horaria FROM formacao_digital WHERE curso = %s;"
        elif table == "FORMAÇÃO EM LÍNGUA BRASILEIRA DE SINAIS":
            return "SELECT curso, sugestao_conteudo, carga_horaria FROM formacao_linguas WHERE curso = %s;"
    
    def get_table_cursos(self, table2):
                       
        if table2 == "FORMAÇÃO DE GESTORES, ESPECIALISTAS E CAPACITAÇÃO DO PESSOAL TÉCNICO - ADMINISTRATIVO":
           return "SELECT curso FROM formacao_gestao;"
        elif table2 == "FORMAÇÃO DIGITAL":
            return "SELECT curso FROM formacao_digital;"
        elif table2 == "FORMAÇÃO EM LÍNGUA BRASILEIRA DE SINAIS":
            return "SELECT curso FROM formacao_linguas;"
    
    def inserir_table(self, arquivo_json):
        with open(arquivo_json, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for chave, item in data.items():
            curso = item.get('Curso', None)
            sugestao_conteudo = item.get('Sugestão de Conteúdo Programático', None)
            carga_horaria = item.get('Carga Horária', None)

            if curso is not None and sugestao_conteudo is not None and carga_horaria is not None:
                # Use self.conn e self.cursor, pois estamos dentro do bloco with
                self.cursor.execute(
                    "INSERT INTO formacao_linguas (id, curso, sugestao_conteudo, carga_horaria) VALUES (%s, %s, %s, %s)",
                    (chave, curso, sugestao_conteudo, carga_horaria)
                )
            else:
                print(f"Faltando informações para a chave {chave}. Inserção ignorada.")

        # Commit e fechamento do cursor são automáticos no final do bloco with
        
    
    def pegar_cursos(self, table):
        try:
            with self:
                query = self.get_table_cursos(table)

                # Execute a consulta SQL com parâmetros
                self.cursor.execute(query)

                # Obtenha os resultados
                results = self.cursor.fetchall()

                cursos = [str(result[0]) for result in results]

                return cursos

        except Exception as e:
            print(f"Erro ao pegar cursos: {str(e)}")
            return []

    def obter_curso(self, curso, table):
        try:
            with self:
                query = self.get_table(table)

                # Execute a consulta SQL com parâmetros
                self.cursor.execute(query, (curso,))

                # Obtenha os resultados
                results = self.cursor.fetchall()

                return results
            
        except Exception as e:
            print(f"Erro ao obter curso: {str(e)}")
            return ""
        
    def buscar_curso(self, curso):
        try:
            with self:
                query = "SELECT curso, sugestao_conteudo, carga_horaria FROM formacao_gestao WHERE curso = %s UNION SELECT curso, sugestao_conteudo, carga_horaria FROM formacao_digital WHERE curso = %s UNION SELECT curso, sugestao_conteudo, carga_horaria FROM formacao_linguas WHERE curso = %s"
                self.cursor.execute(query, (curso, curso, curso))
                resultado = self.cursor.fetchall()
                return resultado

        except psycopg2.Error as e:
            print(f"Erro ao obter informações do curso com as tabelas: {e}")
            return None
    
    def get_id(self, usuario):
        try:
            with self:
                self.cursor.execute("SELECT id FROM credenciais WHERE usuario = %s", (usuario,))
                resultado = self.cursor.fetchone()
                return resultado[0]

        except Exception as e:
            print(f"Erro ao obter ID do usuário: {str(e)}")
            return None
    
    def get_id_with_email(self, email):
        try:
            with self:
                self.cursor.execute("SELECT cred_id FROM informacoes_usuario WHERE email = %s", (email,))
                resultado = self.cursor.fetchone()
                return resultado[0]

        except Exception as e:
            print(f"Erro ao obter ID do usuário usando o email: {str(e)}")
            return None
    def get_credenciais(self, id):
        try:
            with self:
                query = "SELECT usuario, senha FROM credenciais WHERE id = %s"
                self.cursor.execute(query, (id,))
                resultado = self.cursor.fetchall()
                return resultado

        except psycopg2.Error as e:
            print(f"Erro ao obter credenciais do usuário: {e}")
            return None
        
    def get_informacoes(self, cred_id):
        try:
            with self:
                query = "SELECT nome, email, secretaria, cpf, celular, matricula, cargo_funcao, vinculo, lotacao FROM informacoes_usuario WHERE cred_id = %s"
                self.cursor.execute(query, (cred_id,))
                resultado = self.cursor.fetchall()
                return resultado

        except psycopg2.Error as e:
            print(f"Erro ao obter informações do usuário: {e}")
            return None
    
    def pegar_dadosecao(self, formulario_id):
        try:
            with self:
                query = "SELECT * FROM informacoes_usuario INNER JOIN formulario_solicitacao ON informacoes_usuario.id = formulario_solicitacao.formulario_id WHERE formulario_solicitacao.formulario_id = %s"
                self.cursor.execute(query, (formulario_id,))
                resultado = self.cursor.fetchall()
                return resultado

        except psycopg2.Error as e:
            print(f"Erro ao obter dados da secretaria e ação: {e}")
            return None
    
    def get_info_id(self, cred_id):
        try:
            with self:
                query = "SELECT id FROM informacoes_usuario WHERE cred_id = %s"
                self.cursor.execute(query, (cred_id,))
                resultado = self.cursor.fetchone()
                return resultado[0]

        except psycopg2.Error as e:
            print(f"Erro ao obter id do usuario: {e}")
            return None
    
    def alterar_dados(self, cred_id, nome, email, secretaria, cpf, celular, matricula, cargo_funcao, vinculo, lotacao):
        try:
            with self:
                query = "UPDATE informacoes_usuario SET nome=%s, email=%s, secretaria=%s, cpf=%s, celular=%s, matricula=%s, cargo_funcao=%s, vinculo=%s, lotacao=%s WHERE cred_id=%s"
                novos_dados = (nome, email, secretaria, cpf, celular, matricula, cargo_funcao, vinculo, lotacao, cred_id)
                self.cursor.execute(query, novos_dados)
                self.conn.commit()
                return True

        except psycopg2.Error as e:
            print(f"Erro ao alterar os dados do usuário: {e}")
            self.conn.rollback()
            return False
    
    def alterar_credenciais(self, id, usuario, senha, pass_type):
        try:
            with self:
                if not pass_type:
                    senha = self.hash_password(senha)
                else:
                    senha = bytes.fromhex(senha)

                query = "UPDATE credenciais SET usuario=%s, senha=%s WHERE id=%s"
                novas_credenciais = (usuario, senha, id)
                self.cursor.execute(query, novas_credenciais)
                self.conn.commit()
                return True

        except psycopg2.Error as e:
            print(f"Erro ao alterar as credenciais do usuário: {e}")
            self.conn.rollback()
            return False
    
    def verificar_usuario(self, usuario):
        try:
            with self:
                self.cursor.execute("SELECT * FROM credenciais WHERE usuario = %s", (usuario,))
                resultado = self.cursor.fetchone()
                return resultado is not None

        except Exception as e:
            print(f"Erro ao verificar usuário: {str(e)}")
            return False
    
    def verificar_usuario_alteracao(self, usuario, id):
        try:
            with self:
                self.cursor.execute("SELECT * FROM credenciais WHERE usuario = %s AND id != %s", (usuario, id))
                resultado = self.cursor.fetchone()
                return resultado is not None

        except Exception as e:
            print(f"Erro ao verificar usuário: {str(e)}")
            return False
    
    def verificar_senha(self, nome_usuario, senha):
        try:
            with self:
                self.cursor.execute(
                    "SELECT senha FROM credenciais WHERE usuario = %s",
                    (nome_usuario,)
                )
                resultado = self.cursor.fetchone()

                if not resultado:
                    return False

                hash_armazenado = bytes(resultado[0])

                return bcrypt.checkpw(
                    senha.encode("utf-8"),
                    hash_armazenado
                )

        except Exception as e:
            print(f"Erro ao verificar senha: {e}")
            return False
    
    def verificar_senha_alteracao(self, senha_digitada, id):
        try:
            with self:
                self.cursor.execute(
                    "SELECT senha FROM credenciais WHERE id != %s",
                    (id,)
                )
                resultados = self.cursor.fetchall()

                for resultado in resultados:
                    hash_armazenado = bytes(resultado[0])

                    if bcrypt.checkpw(
                        senha_digitada.encode("utf-8"),
                        hash_armazenado
                    ):
                        return True

                return False

        except Exception as e:
            print(f"Erro ao verificar senha: {e}")
            return False
        
    def verificar_senha_nova_conta(self, senha_digitada):
        try:
            with self:
                self.cursor.execute("SELECT senha FROM credenciais")
                resultados = self.cursor.fetchall()

                for resultado in resultados:
                    hash_armazenado = bytes(resultado[0])

                    if bcrypt.checkpw(
                        senha_digitada.encode("utf-8"),
                        hash_armazenado
                    ):
                        return True

                return False

        except Exception as e:
            print(f"Erro ao verificar senha da nova conta: {e}")
            return False
    
    def adicionar_usuario_senha(self, usuario, senha):
        try:
            with self:
                hash_senha = self.hash_password(senha)
                self.cursor.execute("INSERT INTO credenciais (usuario, senha) VALUES (%s, %s)", (usuario, hash_senha))
                self.conn.commit()
        except Exception as e:
            print(f"Erro ao adicionar usuário e senha: {e}")
            self.conn.rollback()
            return False
    
    def criar_conta(self, usuario, senha, nome, email, secretaria, cpf, telefone, matricula, cargo, vinculo, lotacao):
        try:
            with self:
                # Insere as credenciais e recupera o ID
                self.cursor.execute(
                    """
                    INSERT INTO credenciais (usuario, senha)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (usuario, self.hash_password(senha))
                )

                id_credencial = self.cursor.fetchone()[0]

                # Insere as informações pessoais
                self.cursor.execute(
                    """
                    INSERT INTO informacoes_usuario
                    (cred_id, nome, email, secretaria, cpf, celular,
                    matricula, cargo_funcao, vinculo, lotacao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        id_credencial, nome, email, secretaria, cpf,
                        telefone, matricula, cargo, vinculo, lotacao
                    )
                )

                # Confirma as duas operações juntas
                self.conn.commit()
                return True

        except Exception as e:
            print(f"Erro ao adicionar a nova conta ao sistema: {e}")

            if self.conn is not None:
                self.conn.rollback()

            return False
    
    def gravar_solicitacao(self, id_info, nome_acao, tipo_acao, num_vagas, carga_horaria, data_inicio, data_fim, turno, modalidade, publico, justificativa, objetivo, sugestao):
        try:
            with self:
                # Insere na tabela formulario_solicitacao e retorna o ID da linha recém-adicionada

                self.cursor.execute("""
                    INSERT INTO formulario_solicitacao 
                    (formulario_id, nome_acao, tipo_acao, num_vagas, carga_horaria, data_inicio, data_fim, turno, modalidade, publico_alvo, justificativa, objetivo, sugestao) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (id_info, nome_acao, tipo_acao, num_vagas, carga_horaria, data_inicio, data_fim, turno, modalidade, publico, justificativa, objetivo, sugestao))
                
                # Recupera o ID da linha recém-adicionada
                inserted_id = self.cursor.fetchone()[0]
                
                self.conn.commit()
                
                return inserted_id

        except Exception as e:
            print(f"Erro ao regristrar ação no sistema: {e}")
            self.conn.rollback()
            return None

    
    def gravar_listagem(self, nome, matricula, telefone, email, solicitacao_id):
        
        try:
            with self:
                # Insere na tabela listagem_servidores

                self.cursor.execute("INSERT INTO listagem_servidores (solicitacao_id, nome, matricula, telefone, email) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                            (solicitacao_id, nome, matricula, telefone, email))
                # Recupera o ID da linha recém-adicionada
                inserted_id = self.cursor.fetchone()[0]
                
                self.conn.commit()
                
                return inserted_id

        except Exception as e:
            print(f"Erro ao regristrar listagem de servidores no sistema: {e}")
            self.conn.rollback()
            return None
    
    def gravar_historico_insercao(self, listagem_servidores_id, detalhes):
        try:
            with self:
                # Obter a data e hora atuais
                data_hora_atual_nformatada = datetime.datetime.now()
                
                data_hora_atual = data_hora_atual_nformatada.strftime("%Y-%m-%d %H:%M:%S")
                
                # Insere na tabela historico_alteracoes_servidores
                self.cursor.execute("""
                    INSERT INTO historico_alteracoes_servidores
                    (listagem_servidores_id, data_hora, tipo_alteracao, detalhes)
                    VALUES (%s, %s, %s, %s)
                """, (listagem_servidores_id, data_hora_atual, "Inserção", detalhes))
                
                self.conn.commit()
                return True

        except Exception as e:
            print(f"Erro ao inserir novo histórico de alterações dos servidores no sistema: {e}")
            self.conn.rollback()
            return False
        
    def hash_password(self, password):
        self.salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), self.salt)
        return self.hashed_password
    
    def validar_criacao(self, username, password):
        if _contem_caracteres_especiais(username):
            return False
        if not self.verificar_usuario(username):
            if not self.verificar_senha_nova_conta(password):
                return True
            else:
                return False
        else:
            return False

    def validar_login(self, username, password):
        if _contem_caracteres_especiais(username):
            return False
        if self.verificar_usuario(username):
            if self.verificar_senha(username, password):
                return True
            else:
                return False
        else:
            return False
    
    
    def validar_alteracao(self, username, password, tipo_senha, id):
        print("inicio funcao validacao")
        if _contem_caracteres_especiais(username):
            return False
        print(username)
        if not self.verificar_usuario_alteracao(username, id):
            print("usuario verificado")
            if not tipo_senha:
                print("senha n é hexadecimal")
                if not self.verificar_senha_alteracao(password, id):
                    print("senha esta ok")
                    return True
                else:
                    return False
            else:
                print("senha é hexadecimal")
                return True
        else:
            print("teste saida")
            return False

        

