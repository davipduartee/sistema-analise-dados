# Graph Report - sistema-analise-dados  (2026-10-16)

## Corpus Check
- Corpus is ~2,002 words - fits in a single context window. You may not need a graph.

## Summary
- 63 nodes · 124 edges · 7 communities
- Extraction: 74% EXTRACTED · 26% INFERRED · 0% AMBIGUOUS · INFERRED: 32 edges (avg confidence: 0.92)
- Token cost: 72,656 input · 0 output

## Community Hubs (Navigation)
- Hierarquia de Exceções
- Validadores com Regex
- Relatório e Visão Geral
- Validação de Data e Idade
- CLI e Ponto de Entrada
- Leitura do CSV
- Erros de Arquivo

## God Nodes (most connected - your core abstractions)
1. `FormatoInvalidoError` - 13 edges
2. `ValidacaoError` - 10 edges
3. `ler_csv()` - 8 edges
4. `validar_registro()` - 8 edges
5. `main()` - 8 edges
6. `Sistema de Análise de Dados em Python` - 8 edges
7. `IdadeInvalidaError` - 7 edges
8. `DataFuturaError` - 7 edges
9. `validar_data()` - 6 edges
10. `Validação com Expressões Regulares (re)` - 6 edges

## Surprising Connections (you probably didn't know these)
- `dados/clientes.csv` --shares_data_with--> `ler_csv()`  [INFERRED]
  README.md → main.py
- `Padrão regex de data (dd/mm/aaaa)` --references--> `DataFuturaError`  [INFERRED]
  README.md → excecoes.py
- `FileNotFoundError` --references--> `ler_csv()`  [EXTRACTED]
  README.md → main.py
- `Rejeição de campos vazios` --implements--> `validar_registro()`  [INFERRED]
  README.md → main.py
- `ValueError` --references--> `validar_registro()`  [INFERRED]
  README.md → main.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fluxo de tratamento de erros de arquivo (try/except/else/finally)** — readme_try_except_else_finally, readme_filenotfounderror, readme_keyerror, readme_oserror, main_main [EXTRACTED 1.00]
- **Pipeline de validação de campos do CSV** — readme_validacao_regex, validadores_validar_nome, validadores_validar_email, validadores_validar_cpf, validadores_validar_telefone, validadores_validar_data, validadores_validar_idade, main_validar_registro [INFERRED 0.95]
- **Hierarquia de ValidacaoError** — excecoes_validacaoerror, excecoes_formatoinvalidoerror, excecoes_idadeinvalidaerror, excecoes_datafuturaerror, readme_excecoes_personalizadas [EXTRACTED 1.00]

## Communities (7 total, 0 thin omitted)

### Community 0 - "Hierarquia de Exceções"
Cohesion: 0.23
Nodes (5): DataFuturaError, FormatoInvalidoError, ValidacaoError, validar_registro(), Rejeição de campos vazios

### Community 1 - "Validadores com Regex"
Cohesion: 0.23
Nodes (8): Padrão regex de CPF, Padrão regex de e-mail, Padrão regex de nome, Padrão regex de telefone, validar_cpf(), validar_email(), validar_nome(), validar_telefone()

### Community 2 - "Relatório e Visão Geral"
Cohesion: 0.18
Nodes (6): dados/clientes.csv, Desafio Sprint 5 (Semana 05), Relatório formatado com f-strings, saida/relatorio.txt, Sistema de Análise de Dados em Python, _cortar()

### Community 3 - "Validação de Data e Idade"
Cohesion: 0.39
Nodes (7): IdadeInvalidaError, datetime.strptime, Faixa de idade 18 a 120 anos, Padrão regex de data (dd/mm/aaaa), ValueError, validar_data(), validar_idade()

### Community 4 - "CLI e Ponto de Entrada"
Cohesion: 0.43
Nodes (3): main(), Interface de linha de comando (arquivo, -o), gerar_relatorio()

### Community 5 - "Leitura do CSV"
Cohesion: 0.50
Nodes (3): ler_csv(), dados/clientes_sem_telefone.csv, KeyError

### Community 6 - "Erros de Arquivo"
Cohesion: 0.50
Nodes (3): FileNotFoundError, OSError, salvar_relatorio()

## Knowledge Gaps
- **1 isolated node(s):** `Desafio Sprint 5 (Semana 05)`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 17 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FormatoInvalidoError` connect `Hierarquia de Exceções` to `Validadores com Regex`, `Validação de Data e Idade`, `CLI e Ponto de Entrada`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `ler_csv()` (e.g. with `dados/clientes.csv` and `dados/clientes_sem_telefone.csv`) actually correct?**
  _`ler_csv()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Desafio Sprint 5 (Semana 05)` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Why does `Sistema de Análise de Dados em Python` connect `Relatório e Visão Geral` to `Hierarquia de Exceções`, `Validadores com Regex`, `CLI e Ponto de Entrada`, `Leitura do CSV`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `validar_registro()` (e.g. with `ValidacaoError` and `Rejeição de campos vazios`) actually correct?**
  _`validar_registro()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Why does `ValidacaoError` connect `Hierarquia de Exceções` to `Validação de Data e Idade`, `CLI e Ponto de Entrada`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `main()` (e.g. with `Interface de linha de comando (arquivo, -o)` and `Blocos try/except/else/finally`) actually correct?**
  _`main()` has 2 INFERRED edges - model-reasoned connections that need verification._