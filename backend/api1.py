from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from backend.tokens import generate_token, generate_recovery_token, pegar_id_com_token
from backend.banco_de_dados import Banco
from frontend.funcoes_paginas import gerar_solicitacao, gerar_sugestao
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from smtplib import SMTPAuthenticationError
from pydantic import BaseModel
import streamlit as st
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


class MyFastAPI:
    def __init__(self):
        self.app = FastAPI()

        # Configuração do CORS
        origins = ["http://192.168.1.84:5001/"]
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

        self.banco = Banco()

        # Configuração do FastMail
        self.mail_config = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
            MAIL_FROM=os.getenv("MAIL_FROM", ""),
            MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
            MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

        self.mail = FastMail(self.mail_config)

        self.configurar_rotas()

    def configurar_rotas(self):
        self.app.post(
            "/login",
            response_model=dict,
            description="Realiza login e gera um token de acesso.",
        )(self.login)
        self.app.post(
            "/esqueceu_senha",
            response_model=dict,
            description="Envia um e-mail de recuperação de senha.",
        )(self.esqueceu_senha)
        self.app.post(
            "/criar_conta",
            response_model=dict,
            description="Cria uma nova conta de usuário.",
        )(self.criar_conta)
        self.app.post(
            "/alterar_conta",
            response_model=dict,
            description="Altera a conta do usuário.",
        )(self.alterar_conta)
        self.app.get("/dados", description="Pega os dados do usuário.")(
            self.dados
        )
        self.app.post(
            "/enviar_solicitacao",
            response_model=dict,
            description="Recebe os dados da solicitação.",
        )(self.enviar_solicitacao)
        self.app.post(
            "/enviar_sugestao",
            response_model=dict,
            description="Recebe os dados da sugestão.",
        )(self.enviar_sugestao)

    class CriarContaRequest(BaseModel):
        novo_usuario: str
        nova_senha: str
        nome: str
        email: str
        cpf: str
        telefone: str
        secretaria: str
        lotacao: str
        matricula: str
        cargo: str
        vinculo: str

    class AlterarContaRequest(BaseModel):
        id: str
        usuario: str
        senha: str
        tipo_senha: bool
        nome: str
        email: str
        cpf: str
        telefone: str
        secretaria: str
        lotacao: str
        matricula: str
        cargo: str
        vinculo: str
        
    def criar_conta(self, request: CriarContaRequest):
        try:
            if self.banco.validar_criacao(request.novo_usuario, request.nova_senha):
                if self.banco.criar_conta(
                    request.novo_usuario,
                    request.nova_senha,
                    request.nome,
                    request.email,
                    request.secretaria,
                    request.cpf,
                    request.telefone,
                    request.matricula,
                    request.cargo,
                    request.vinculo,
                    request.lotacao,
                ):
                    return {"mensagem": "Conta criada com sucesso."}
            else:
                raise HTTPException(
                    status_code=409, detail="Usuário ou senha já existem."
                )
        except HTTPException as http_error:
            raise HTTPException(
                status_code=http_error.status_code,
                detail=http_error.detail
            )       
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def alterar_conta(self, request: AlterarContaRequest):
        try:
            print("DEBUG: validando alteracao...")
            print("DEBUG:", request.senha)
            print("DEBUG:", request.tipo_senha)
            if self.banco.validar_alteracao(
                request.usuario, request.senha, request.tipo_senha, request.id
            ): 
                print("DEBUG: validar alteracao - concluida")
                if self.banco.alterar_dados(
                    request.id,
                    request.nome,
                    request.email,
                    request.secretaria,
                    request.cpf,
                    request.telefone,
                    request.matricula,
                    request.cargo,
                    request.vinculo,
                    request.lotacao,
                ) and self.banco.alterar_credenciais(
                    request.id, request.usuario, request.senha, request.tipo_senha
                ):
                    return {"mensagem": "Conta alterada com sucesso."}
            else:
                raise HTTPException(
                    status_code=401, detail="Usuário ou senha já existem."
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def enviar_solicitacao(self, acoes_preenchidas: List[dict]):
        try:
            print("DEBUG:", "gerando documentos...")
            documentos = gerar_solicitacao(acoes_preenchidas, "backend/formulario_modelo.docx", "backend")
            print("DEBUG:", "enviando email...")
            await self.enviar_email_documentos("capacitacao@eggem.saoluis.ma.gov.br", documentos)
            return {"mensagem": "Documento gerado e email de solicitação enviado com sucesso."}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def enviar_sugestao(self, dados_acoes: dict):
        try:
            print("DEBUG:", "gerando documento...")
            documento = gerar_sugestao(dados_acoes, "backend/formulario_modelo.docx", "backend")
            print("DEBUG:", "enviando email...")
            await self.enviar_email_documento("capacitacao@eggem.saoluis.ma.gov.br", documento)
            return {"mensagem": "Documento gerado e email de solicitação enviado com sucesso."}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def login(self, user_and_pass: dict):
        try:
            usuario = user_and_pass.get("usuario")
            senha = user_and_pass.get("senha")
            if self.banco.validar_login(usuario, senha):
                token_generated = generate_token(self.banco.get_id(usuario))
                return {"token": token_generated, "mensagem": "Login bem-sucedido."}
            else:
                raise HTTPException(status_code=401, detail="Credenciais inválidas. Acesso negado.")
        except HTTPException as http_error:
            raise HTTPException(
                status_code=http_error.status_code,
                detail=http_error.detail
            )       
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def dados(self, token_dict: dict):
        id = pegar_id_com_token(token_dict.get("token").encode('utf-8'))
        informacoes = self.banco.get_informacoes(id)
        credenciais = self.banco.get_credenciais(id)
        senha_hex = bytes(credenciais[0][1]).hex()
        return {"nome": informacoes[0][0],
                "email": informacoes[0][1],
                "secretaria": informacoes[0][2],
                "cpf": informacoes[0][3],
                "telefone": informacoes[0][4],
                "matricula": informacoes[0][5],
                "cargo": informacoes[0][6],
                "vinculo": informacoes[0][7],
                "lotacao": informacoes[0][8],
                "usuario": credenciais[0][0],
                "senha": senha_hex,
                "id": str(id)}

    async def esqueceu_senha(self, dados_email: dict):
        try:
            email = dados_email.get("email")
            user_id = self.banco.get_id_with_email(email)
            print(f"DEBUG: user_id - {user_id}")

            if user_id is not None:
                token_pass = generate_recovery_token(user_id)
                await self.enviar_email_recuperacao(email, token_pass)
                return {
                    "token_pass": token_pass,
                    "mensagem_pass": "E-mail de recuperação enviado com sucesso.",
                }
            else:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Chave não encontrada: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def enviar_email_recuperacao(self, email: str, token: str):
        try:
            message = MessageSchema(
                subject="Recuperação de Senha",
                recipients=[email],
                body=f"Clique no link a seguir para recuperar sua senha http://seu_site.com/redefinir_senha/{token}",
                subtype="plain",
            )
            await self.mail.send_message(message)
        except SMTPAuthenticationError as e:
            mensagem_erro = str(e)
            if "Username and Password not accepted" in mensagem_erro:
                raise HTTPException(
                    status_code=401,
                    detail="Erro de autenticação: O nome de usuário ou senha está incorreto.",
                )
            else:
                raise HTTPException(
                    status_code=500, detail=f"Erro de autenticação: {mensagem_erro}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao enviar e-mail de recuperação para {email}: {str(e)}",
            )

    async def enviar_email_documentos(self, email: str, caminhos_documentos: List[Dict[str, Any]]):
        try:
            primeiro_documento = caminhos_documentos[0]
            secretaria = primeiro_documento["secretaria"]
            ano_atual = primeiro_documento["ano_atual"]
            print("DEBUG: Dados do documento pegos...")
            
            attachments = [{"file": caminho["caminho"], "filename": caminho["caminho"].split("/")[-1]} for caminho in caminhos_documentos]

            message = MessageSchema(
                subject=f"Solicitação D.E {secretaria} {ano_atual}",
                recipients=[email],
                body=f"Segue em anexo o(s) documento(s) gerado(s) referente(s) à solicitação D.E {secretaria} {ano_atual}.",
                subtype="plain",
                attachments=attachments,
            )
            
            print("DEBUG: Corpo do email montado...")
            
            await self.mail.send_message(message)
            
        except FileNotFoundError as file_error:
            print("DEBUG: Arquivo não encontrado:", str(file_error))
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao enviar email com o(s) documento(s) da solicitação para {email}: Arquivo não encontrado."
            )
        except Exception as e:
            print("DEBUG: Erro durante o envio do email:", str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao enviar email com o(s) documento(s) da solicitação para {email}: {str(e)}"
            )
            
    async def enviar_email_documento(self, email: str, caminhos_documentos: List[Dict[str, Any]]):
        try:
            primeiro_documento = caminhos_documentos[0]
            secretaria = primeiro_documento["secretaria"]
            ano_atual = primeiro_documento["ano_atual"]
            print("DEBUG: Dados do documento pegos...")
            
            attachments = [{"file": caminho["caminho"], "filename": caminho["caminho"].split("/")[-1]} for caminho in caminhos_documentos]

            message = MessageSchema(
                subject=f"Sugestão D.E {secretaria} {ano_atual}",
                recipients=[email],
                body=f"Segue em anexo o documento gerado referente à sugestão D.E {secretaria} {ano_atual}.",
                subtype="plain",
                attachments=attachments,
            )
            
            print("DEBUG: Corpo do email montado...")
            
            await self.mail.send_message(message)
        
        except FileNotFoundError as file_error:
            print("DEBUG: Arquivo não encontrado:", str(file_error))
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao enviar email com o documento da sugestão para {email}: Arquivo não encontrado."
            )
        except Exception as e:
            print("DEBUG: Erro durante o envio do email:", str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao enviar email com o documento da sugestão para {email}: {str(e)}"
            )

fa = MyFastAPI()
