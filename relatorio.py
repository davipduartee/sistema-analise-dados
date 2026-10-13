"""Geração e gravação do relatório final com f-strings."""

from collections import Counter
from datetime import datetime
from pathlib import Path

LARGURA = 100


def _cortar(texto, tamanho):
    """Encurta textos longos para caberem na coluna da tabela."""
    return texto if len(texto) <= tamanho else texto[: tamanho - 1] + "…"


def gerar_relatorio(arquivo_origem, validos, invalidos):
    total = len(validos) + len(invalidos)
    perc_validos = len(validos) / total * 100 if total else 0.0
    perc_invalidos = len(invalidos) / total * 100 if total else 0.0
    erros_por_campo = Counter(campo for _, erros in invalidos for campo, _ in erros)

    linhas = [
        "=" * LARGURA,
        f"{'RELATÓRIO DE ANÁLISE DE DADOS':^{LARGURA}}",
        "=" * LARGURA,
        f"Arquivo analisado : {arquivo_origem}",
        f"Gerado em         : {datetime.now():%d/%m/%Y %H:%M:%S}",
        "",
        "ESTATÍSTICAS",
        "-" * LARGURA,
        f"Total de registros   : {total:>4}",
        f"Registros válidos    : {len(validos):>4}  ({perc_validos:5.1f}%)",
        f"Registros inválidos  : {len(invalidos):>4}  ({perc_invalidos:5.1f}%)",
        "",
        "Erros por campo:",
    ]
    if erros_por_campo:
        for campo, quantidade in erros_por_campo.most_common():
            linhas.append(f"  {campo:<15} {quantidade:>3} ocorrência(s)")
    else:
        linhas.append("  Nenhum erro encontrado.")

    linhas += [
        "",
        f"REGISTROS VÁLIDOS ({len(validos)})",
        "-" * LARGURA,
        f"{'Lin':>3}  {'Nome':<22} {'E-mail':<30} {'CPF':<14} {'Telefone':<16} {'Idade':>5}",
    ]
    for r in validos:
        linhas.append(
            f"{r['linha']:>3}  {_cortar(r['nome'], 22):<22} {_cortar(r['email'], 30):<30} "
            f"{r['cpf']:<14} {r['telefone']:<16} {r['idade']:>5}"
        )

    linhas += ["", f"REGISTROS INVÁLIDOS ({len(invalidos)})", "-" * LARGURA]
    for r, erros in invalidos:
        linhas.append(f"Linha {r['linha']:>3} | {r['nome'] or '(sem nome)'}")
        for _, mensagem in erros:
            linhas.append(f"          - {mensagem}")

    linhas.append("=" * LARGURA)
    return "\n".join(linhas)


def salvar_relatorio(texto, caminho):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto + "\n")
