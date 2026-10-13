"""Funções de validação de cada campo usando o módulo re."""

import re
from datetime import date, datetime

from excecoes import DataFuturaError, FormatoInvalidoError, IdadeInvalidaError

# Nome e sobrenome: só letras (\w sem dígitos e sem "_"), separados por espaço.
PADRAO_NOME = re.compile(r"^[^\W\d_]+(\s[^\W\d_]+)+$")
# usuario@dominio.com — parte local com letras, números, ".", "+", "-".
PADRAO_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)*\.[A-Za-z]{2,}$")
# 000.000.000-00
PADRAO_CPF = re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
# (98) 98765-4321 ou (98) 3214-5678 — espaço após o DDD é opcional.
PADRAO_TELEFONE = re.compile(r"^\(\d{2}\)\s?9?\d{4}-\d{4}$")
# dd/mm/aaaa
PADRAO_DATA = re.compile(r"^\d{2}/\d{2}/\d{4}$")

IDADE_MINIMA = 18
IDADE_MAXIMA = 120


def validar_nome(valor):
    if not PADRAO_NOME.match(valor):
        raise FormatoInvalidoError("nome", valor, "informe nome e sobrenome, apenas letras")


def validar_email(valor):
    if not PADRAO_EMAIL.match(valor):
        raise FormatoInvalidoError("email", valor, "formato esperado usuario@dominio.com")


def validar_cpf(valor):
    if not PADRAO_CPF.match(valor):
        raise FormatoInvalidoError("cpf", valor, "formato esperado 000.000.000-00")

    digitos = [int(d) for d in re.sub(r"\D", "", valor)]
    if len(set(digitos)) == 1:
        raise FormatoInvalidoError("cpf", valor, "todos os dígitos são iguais")

    # Confere os dois dígitos verificadores (pesos 10..2 e depois 11..2).
    for posicao in (9, 10):
        soma = sum(d * peso for d, peso in zip(digitos[:posicao], range(posicao + 1, 1, -1)))
        if digitos[posicao] != soma * 10 % 11 % 10:
            raise FormatoInvalidoError("cpf", valor, "dígito verificador não confere")


def validar_telefone(valor):
    if not PADRAO_TELEFONE.match(valor):
        raise FormatoInvalidoError("telefone", valor, "formato esperado (00) 00000-0000")


def validar_data(valor):
    if not PADRAO_DATA.match(valor):
        raise FormatoInvalidoError("data_cadastro", valor, "formato esperado dd/mm/aaaa")

    # strptime lança ValueError para datas inexistentes, como 31/02/2024.
    data = datetime.strptime(valor, "%d/%m/%Y").date()
    if data > date.today():
        raise DataFuturaError("data_cadastro", valor, "a data não pode estar no futuro")


def validar_idade(valor):
    idade = int(valor)  # lança ValueError se o texto não for um número inteiro
    if not IDADE_MINIMA <= idade <= IDADE_MAXIMA:
        raise IdadeInvalidaError(
            "idade", valor, f"deve estar entre {IDADE_MINIMA} e {IDADE_MAXIMA} anos"
        )


# Campo do CSV -> função que o valida. A ordem define a ordem das colunas obrigatórias.
VALIDADORES = {
    "nome": validar_nome,
    "email": validar_email,
    "cpf": validar_cpf,
    "telefone": validar_telefone,
    "data_cadastro": validar_data,
    "idade": validar_idade,
}
