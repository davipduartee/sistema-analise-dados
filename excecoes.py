"""Exceções personalizadas para as regras de negócio do sistema."""


class ValidacaoError(Exception):
    """Classe base para todos os erros de validação de um campo."""

    def __init__(self, campo, valor, motivo):
        self.campo = campo
        self.valor = valor
        self.motivo = motivo
        super().__init__(f"{campo} '{valor}': {motivo}")


class FormatoInvalidoError(ValidacaoError):
    """O valor não segue o padrão (regex) esperado para o campo."""


class IdadeInvalidaError(ValidacaoError):
    """A idade está fora da faixa aceita pela regra de negócio."""


class DataFuturaError(ValidacaoError):
    """A data informada ainda não aconteceu."""
