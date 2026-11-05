import os
import jwt
from dotenv import load_dotenv

load_dotenv()
from datetime import datetime, timedelta, timezone

# Chave secreta para assinar e verificar os tokens
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY or SECRET_KEY == "SUBSTITUA_POR_UMA_CHAVE_ALEATORIA_LONGA":
    raise RuntimeError(
        "SECRET_KEY não configurada. Defina uma chave segura no arquivo .env."
    )


def generate_recovery_token(email):
    expiration_time = datetime.now(timezone.utc) + timedelta(hours=2)
    payload = {"email": email, "exp": expiration_time}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def generate_token(user_id):
    expiration_time = datetime.now(timezone.utc) + timedelta(hours=2)
    payload = {"user_id": user_id, "exp": expiration_time}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verificar_exp_token(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.InvalidTokenError:
        return False


def pegar_id_com_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload.get("user_id")
