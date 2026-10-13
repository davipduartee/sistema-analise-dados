"""Sistema de Análise de Dados — Desafio Sprint 5.

Lê um CSV de clientes, valida cada campo com regex e gera um relatório.

Uso:
    python main.py                                   # usa dados/clientes.csv
    python main.py dados/outro.csv -o saida/rel.txt
"""

import argparse
import csv
import sys

from excecoes import FormatoInvalidoError, ValidacaoError
from relatorio import gerar_relatorio, salvar_relatorio
from validadores import VALIDADORES

CAMPOS_OBRIGATORIOS = tuple(VALIDADORES)


def ler_csv(caminho):
    """Lê o CSV e devolve uma lista de dicionários só com os campos obrigatórios.

    Lança FileNotFoundError se o arquivo não existir e KeyError se faltar coluna.
    """
    registros = []
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        # A linha 1 é o cabeçalho, então os dados começam na linha 2.
        for numero_linha, linha in enumerate(leitor, start=2):
            registro = {campo: (linha[campo] or "").strip() for campo in CAMPOS_OBRIGATORIOS}
            registro["linha"] = numero_linha
            registros.append(registro)
    return registros


def validar_registro(registro):
    """Valida todos os campos e devolve a lista de erros como (campo, mensagem)."""
    erros = []
    for campo, validar in VALIDADORES.items():
        valor = registro[campo]
        try:
            if not valor:
                raise FormatoInvalidoError(campo, valor, "campo obrigatório vazio")
            validar(valor)
        except ValidacaoError as erro:
            erros.append((campo, str(erro)))
        except ValueError as erro:
            erros.append((campo, f"{campo} '{valor}': conversão de tipo inválida ({erro})"))
    return erros


def main():
    parser = argparse.ArgumentParser(description="Valida um CSV de clientes e gera um relatório.")
    parser.add_argument("arquivo", nargs="?", default="dados/clientes.csv", help="CSV de entrada")
    parser.add_argument("-o", "--saida", default="saida/relatorio.txt", help="arquivo do relatório")
    args = parser.parse_args()

    try:
        registros = ler_csv(args.arquivo)
    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {args.arquivo}")
        return 1
    except KeyError as erro:
        print(f"[ERRO] Coluna obrigatória ausente no CSV: {erro}")
        print(f"       Colunas esperadas: {', '.join(CAMPOS_OBRIGATORIOS)}")
        return 1
    else:
        print(f"[OK] {len(registros)} registro(s) lido(s) de {args.arquivo}")
    finally:
        print("[INFO] Etapa de leitura encerrada.")

    validos, invalidos = [], []
    for registro in registros:
        erros = validar_registro(registro)
        if erros:
            invalidos.append((registro, erros))
        else:
            validos.append(registro)

    relatorio = gerar_relatorio(args.arquivo, validos, invalidos)
    print()
    print(relatorio)

    try:
        salvar_relatorio(relatorio, args.saida)
    except OSError as erro:
        print(f"[ERRO] Não foi possível salvar o relatório: {erro}")
        return 1
    else:
        print(f"[OK] Relatório salvo em {args.saida}")
    finally:
        print("[INFO] Processamento finalizado.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
