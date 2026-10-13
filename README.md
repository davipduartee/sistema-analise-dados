# Sistema de Análise de Dados em Python

Entregável da **Semana 05 (Desafio Sprint 5)**. O programa lê um arquivo CSV de clientes, valida e-mail, CPF, telefone, data e idade com **expressões regulares (`re`)**, trata os erros com **`try/except/else/finally`** e **exceções personalizadas**, e gera um **relatório formatado com f-strings**, exibido no terminal e salvo em arquivo.

## Estrutura do projeto

```
sistema-analise-dados/
├── main.py                       # Script principal: leitura do CSV, validação e fluxo de exceções
├── validadores.py                # Padrões regex e funções de validação de cada campo
├── excecoes.py                   # Exceções personalizadas (herdam de Exception)
├── relatorio.py                  # Montagem do relatório com f-strings e gravação em arquivo
├── dados/
│   ├── clientes.csv              # Arquivo de exemplo com registros válidos e inválidos
│   └── clientes_sem_telefone.csv # Arquivo sem a coluna "telefone" (demonstra o KeyError)
└── saida/
    └── relatorio.txt             # Gerado automaticamente ao executar
```

## Como executar

Requer Python 3.8+ e nenhuma biblioteca externa.

```bash
python main.py
```

Com outro arquivo de entrada e outro destino para o relatório:

```bash
python main.py dados/clientes.csv -o saida/relatorio.txt
```

## Validações aplicadas (regex)

Todos os padrões usam *raw strings* (`r"..."`) e são ancorados com `^` (início) e `$` (fim), para que o valor inteiro siga o formato e não apenas um trecho dele.

| Campo | Padrão | Justificativa |
|---|---|---|
| `nome` | `^[^\W\d_]+(\s[^\W\d_]+)+$` | Exige nome **e** sobrenome separados por espaço (`\s`). `[^\W\d_]` aceita só letras, inclusive acentuadas (`\w` sem dígitos e sem `_`). |
| `email` | `^[\w.+-]+@[\w-]+(\.[\w-]+)*\.[A-Za-z]{2,}$` | Parte local com letras, números, `.`, `+` e `-`; um único `@`; domínio terminando em extensão de pelo menos 2 letras (`.com`, `.br`, `.com.br`). |
| `cpf` | `^\d{3}\.\d{3}\.\d{3}-\d{2}$` | Formato `000.000.000-00`. Os pontos são escapados (`\.`) porque `.` sozinho casa com qualquer caractere. Depois do regex, o programa também confere os **dígitos verificadores** e rejeita CPFs com todos os dígitos iguais. |
| `telefone` | `^\(\d{2}\)\s?9?\d{4}-\d{4}$` | DDD entre parênteses, espaço opcional (`\s?`), `9` opcional para celular e número `0000-0000`. Aceita fixo e celular. |
| `data_cadastro` | `^\d{2}/\d{2}/\d{4}$` | Formato `dd/mm/aaaa`. Depois do regex, `datetime.strptime` confirma que a data existe (31/02 é rejeitado) e a regra de negócio impede datas no futuro. |
| `idade` | sem regex: convertida com `int()` | Demonstra o `ValueError` de conversão de tipo. Também deve estar entre 18 e 120 anos. |

Campos vazios são rejeitados antes de qualquer validação.

## Exceções tratadas

| Exceção | Onde ocorre | Como é tratada |
|---|---|---|
| `FileNotFoundError` | `open()` em `ler_csv` quando o arquivo não existe | Mensagem de erro e encerramento com código 1. |
| `KeyError` | Acesso `linha[campo]` quando falta uma coluna obrigatória no CSV | Informa qual coluna está ausente e lista as colunas esperadas. |
| `ValueError` | `int("vinte")` na idade, ou `strptime("31/02/2024")` na data | O registro é marcado como inválido com o motivo; o programa continua. |
| `OSError` | Falha ao gravar o relatório (ex.: sem permissão) | Mensagem de erro e encerramento com código 1. |

Uso dos blocos em `main.py`:

- **`try`**: executa a leitura do CSV (ou a gravação do relatório).
- **`except`**: captura cada tipo de erro separadamente, com uma mensagem específica.
- **`else`**: só roda se não houve erro, e confirma quantos registros foram lidos.
- **`finally`**: roda **sempre**, com erro ou sem erro, e informa o fim da etapa. Ele roda até quando o `except` faz `return`.

### Exceções personalizadas (`excecoes.py`)

```
Exception
└── ValidacaoError           # base: guarda campo, valor e motivo
    ├── FormatoInvalidoError # valor fora do padrão regex, CPF com dígito errado, campo vazio
    ├── IdadeInvalidaError   # idade fora da faixa de 18 a 120 anos
    └── DataFuturaError      # data de cadastro posterior a hoje
```

Como todas herdam de `ValidacaoError`, um único `except ValidacaoError` captura qualquer regra de negócio violada, e cada erro carrega o campo, o valor e o motivo para o relatório.

## Exemplo de entrada (`dados/clientes.csv`)

```csv
nome,email,cpf,telefone,data_cadastro,idade
Ana Beatriz Souza,ana.souza@gmail.com,529.982.247-25,(98) 98765-4321,15/03/2024,28
Carlos Eduardo Lima,carlos.lima@ceuma.br,111.444.777-35,(98) 3214-5678,02/01/2023,45
João Pedro Martins,joao_pedro@outlook.com,123.456.789-09,(11)91234-5678,30/11/2022,19
Mariana Costa,mariana.costa@empresa.com.br,987.654.321-00,(21) 99876-5432,10/07/2025,33
Rafael Oliveira,rafael.oliveira@gmail,390.533.447-05,(98) 98111-2233,20/05/2024,31
Fernanda Alves,fernanda.alves@yahoo.com,123.456.789-00,(98) 98222-3344,12/08/2023,27
Lucas Pereira,lucas.pereira@gmail.com,12345678909,(98) 98333-4455,05/02/2024,22
Juliana Rocha,juliana.rocha@hotmail.com,714.602.380-01,98 98444-5566,18/09/2024,38
Pedro Henrique Dias,pedro.dias@gmail.com,286.481.120-01,(98) 98555-6677,31/02/2024,41
Beatriz Nunes,beatriz.nunes@gmail.com,845.123.906-42,(98) 98666-7788,2024-04-10,vinte
Gabriel Santos,gabriel.santos@gmail.com,111.111.111-11,(98) 98777-8899,01/06/2024,15
Camila Ferreira,camila.ferreira@gmail.com,529.982.247-25,(98) 98888-9900,25/12/2030,29
Thiago,thiago@@gmail.com,,(98) 98999-0011,10/10/2024,150
```

## Exemplo de saída (`saida/relatorio.txt`)

```
====================================================================================================
                                   RELATÓRIO DE ANÁLISE DE DADOS
====================================================================================================
Arquivo analisado : dados/clientes.csv
Gerado em         : 13/10/2026 19:19:29

ESTATÍSTICAS
----------------------------------------------------------------------------------------------------
Total de registros   :   13
Registros válidos    :    4  ( 30.8%)
Registros inválidos  :    9  ( 69.2%)

Erros por campo:
  cpf               4 ocorrência(s)
  data_cadastro     3 ocorrência(s)
  idade             3 ocorrência(s)
  email             2 ocorrência(s)
  telefone          1 ocorrência(s)
  nome              1 ocorrência(s)

REGISTROS VÁLIDOS (4)
----------------------------------------------------------------------------------------------------
Lin  Nome                   E-mail                         CPF            Telefone         Idade
  2  Ana Beatriz Souza      ana.souza@gmail.com            529.982.247-25 (98) 98765-4321     28
  3  Carlos Eduardo Lima    carlos.lima@ceuma.br           111.444.777-35 (98) 3214-5678      45
  4  João Pedro Martins     joao_pedro@outlook.com         123.456.789-09 (11)91234-5678      19
  5  Mariana Costa          mariana.costa@empresa.com.br   987.654.321-00 (21) 99876-5432     33

REGISTROS INVÁLIDOS (9)
----------------------------------------------------------------------------------------------------
Linha   6 | Rafael Oliveira
          - email 'rafael.oliveira@gmail': formato esperado usuario@dominio.com
Linha   7 | Fernanda Alves
          - cpf '123.456.789-00': dígito verificador não confere
Linha   8 | Lucas Pereira
          - cpf '12345678909': formato esperado 000.000.000-00
Linha   9 | Juliana Rocha
          - telefone '98 98444-5566': formato esperado (00) 00000-0000
Linha  10 | Pedro Henrique Dias
          - data_cadastro '31/02/2024': conversão de tipo inválida (day 31 must be in range 1..29 for month 2 in year 2024)
Linha  11 | Beatriz Nunes
          - data_cadastro '2024-04-10': formato esperado dd/mm/aaaa
          - idade 'vinte': conversão de tipo inválida (invalid literal for int() with base 10: 'vinte')
Linha  12 | Gabriel Santos
          - cpf '111.111.111-11': todos os dígitos são iguais
          - idade '15': deve estar entre 18 e 120 anos
Linha  13 | Camila Ferreira
          - data_cadastro '25/12/2030': a data não pode estar no futuro
Linha  14 | Thiago
          - nome 'Thiago': informe nome e sobrenome, apenas letras
          - email 'thiago@@gmail.com': formato esperado usuario@dominio.com
          - cpf '': campo obrigatório vazio
          - idade '150': deve estar entre 18 e 120 anos
====================================================================================================
```

## Demonstração dos erros de arquivo

Arquivo inexistente (`FileNotFoundError`):

```
$ python main.py dados/nao_existe.csv
[ERRO] Arquivo não encontrado: dados/nao_existe.csv
[INFO] Etapa de leitura encerrada.
```

Coluna ausente (`KeyError`):

```
$ python main.py dados/clientes_sem_telefone.csv
[ERRO] Coluna obrigatória ausente no CSV: 'telefone'
       Colunas esperadas: nome, email, cpf, telefone, data_cadastro, idade
[INFO] Etapa de leitura encerrada.
```

Nos dois casos, a linha `[INFO] Etapa de leitura encerrada.` vem do bloco `finally`, o que mostra que ele roda mesmo quando ocorre erro.
