import re
import streamlit as st
from validate_email_address import validate_email


def validar_usuario(usuario):
    if _contem_caracteres_invalidos(usuario):
        _exibir_aviso(
            "Usuário inválido! O usuário deve conter apenas letras minúsculas ou números, sem acentos."
        )
        return False
    return True


def validar_nome(nome):
    if nome != "":
        if not _contem_apenas_letras(nome):
            _exibir_aviso("Nome inválido! O nome deve conter apenas letras.")
            return False
        return True
    return False


def validar_email(email):
    if email != "":
        if validate_email(email):
            return True
        else:
            _exibir_aviso(
                "E-mail inválido! Por favor, insira um endereço de e-mail válido."
            )
            return False
    else:
        return False


def validar_secretaria(secretaria):
    return secretaria is not None


def validar_CPF(cpf):
    if cpf != "":
        cpf = _remover_caracteres_nao_numericos(cpf)
        if (
            not _validar_tamanho_cpf(cpf)
            or _todos_digitos_iguais(cpf)
            or not _validar_digitos_verificadores_cpf(cpf)
        ):
            _exibir_aviso("CPF inválido.")
            return False
        return True
    return False


def validar_telefone(cel):
    if cel != "":
        if not cel.isdigit() or len(cel) != 11:
            _exibir_aviso(
                "Telefone inválido! Verifique se o número contém o DDD, o 9 e o seu telefone."
            )
            return False
        return True
    return False


def validar_matricula(matricula):
    if matricula != "":
        if not matricula.isdigit():
            _exibir_aviso("Matrícula inválida. A matrícula deve conter apenas números")
            return False
        return True
    return False


def validar_cargo(cargo):
    if cargo != "":
        if not _contem_caracteres_validos_cargo(cargo):
            _exibir_aviso(
                "Cargo inválido. O cargo deve conter apenas letras e caracteres especiais."
            )
            return False
        return True
    return False


def validar_vinculo(vinculo):
    return vinculo is not None


def validar_acao(acao):
    if acao != "":
        if not _contem_apenas_letras_numeros_espacos(acao):
            _exibir_aviso("Campo inválido. O campo deve conter apenas letras e números.")
            return False
        return True
    return False

def validar_justificativaobj(jus):
    if jus.strip() != "":
        linhas = jus.strip().split("\n")
        for linha in linhas:
            if not _contem_apenas_letras_numeros_espacos(linha.strip()):
                _exibir_aviso("Campo inválido. Deve conter apenas letras, números e espaços.")
                return False
        return True
    return False


def validar_sugestao(sugestao):
    if sugestao.strip() != "":
        linhas = sugestao.strip().split("\n")
        primeira_linha = linhas[0].strip()
        if not primeira_linha:
            _exibir_aviso("Campo inválido. A primeira linha não pode estar vazia.")
            return False
        for linha in linhas:
            #print("Linha processada:", linha)
            if not _contem_apenas_letras_numeros_espacos(linha.strip()):
                _exibir_aviso("Campo inválido. Deve conter apenas letras, números e caracteres especiais.")
                return False
        return True
    return False











def validar_senha(senha):
    if senha == "":
        return False
    if len(senha) < 8:
        st.warning("Senha fraca! A senha deve ter pelo menos 8 caracteres.")
        return False
    if not any(c.isupper() for c in senha):
        st.warning("Senha fraca! A senha deve possuir ao menos uma letra maiúscula.")
        return False
    if not any(c.islower() for c in senha):
        st.warning("Senha fraca! A senha deve possuir ao menos uma letra minúscula.")
        return False
    if not any(c.isdigit() for c in senha):
        st.warning("Senha fraca! A senha deve possuir ao menos um número.")
        return False
    return True


def validar_campos_criacao(
    usuario,
    senha,
    nome,
    email,
    secretaria,
    cpf,
    celular,
    matricula,
    cargo,
    vinculo,
    lotacao,
    declaracao
):
    if (
        not usuario
        or not senha
        or not nome
        or not email
        or not secretaria
        or not cpf
        or not celular
        or not matricula
        or not cargo
        or not vinculo
        or not lotacao
        or not declaracao
    ):
        _exibir_aviso("Preencha todos os campos.")
        return False
    return True


def validar_campos_login(usuario, senha):
    if not usuario or not senha:
        _exibir_aviso("Preencha todos os campos.")
        return False
    return True


def _contem_caracteres_especiais(texto):
    return bool(re.search(r"[;'\"]", texto))


def _contem_caracteres_invalidos(texto):
    return bool(re.search(r"[^a-z0-9]", texto))

def _contem_apenas_letras_espacos(texto):
    return bool(re.match(r"^[a-zA-ZÀ-ú\s.!?,:;()\[\]{}'\"-]*$", texto))

def _contem_apenas_letras(texto):
    return bool(re.match(r"^[a-zA-Z\s]+$", texto))

def _contem_apenas_letras_numeros_espacos(texto):
    return bool(re.match(r'^[a-zA-Z0-9\s.,;:!?\(\)\[\]{}\'\"áàâãéèêíìîóòôõúùûÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛçÇº–—/\-]*$', texto))


def _exibir_aviso(mensagem):
    st.warning(mensagem)


def _remover_caracteres_nao_numericos(texto):
    return "".join(filter(str.isdigit, texto))


def _validar_tamanho_cpf(cpf):
    return len(cpf) == 11


def _todos_digitos_iguais(cpf):
    return len(set(cpf)) == 1


def _validar_digitos_verificadores_cpf(cpf):
    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto1 = (soma1 * 10) % 11
    digito1 = 0 if resto1 == 10 or resto1 == 11 else resto1

    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto2 = (soma2 * 10) % 11
    digito2 = 0 if resto2 == 10 or resto2 == 11 else resto2

    return int(cpf[9]) == digito1 and int(cpf[10]) == digito2


def _contem_caracteres_validos_cargo(texto):
    padrao = re.compile(r"^[a-zA-ZÀ-ÖØ-öø-ÿ\s!@#$%^&*()_+={}\[\]:;<>,.?/~`|°-]+$")
    return bool(padrao.match(texto))

