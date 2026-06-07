# Relatorio Tecnico do Experimento CI/CD

## 1. Objetivo

Medir e analisar o comportamento de um pipeline CI/CD executado no GitHub
Actions a partir de execucoes reais, coletando metricas de duracao, estabilidade,
falhas, volume de testes e impacto de configuracoes como cache e paralelismo.

## 2. Projeto analisado

O projeto utilizado e uma biblioteca Python simples chamada `task_metrics`.
Ela calcula estatisticas de tarefas, como quantidade total, quantidade por
status, percentual de conclusao e prioridade media.

O projeto foi escolhido por permitir variacoes controladas sem depender de banco
de dados, frontend ou infraestrutura externa.

Repositorio:

- Link: `INSERIR_LINK_DO_REPOSITORIO`

Workflow principal:

- Link do YAML: `INSERIR_LINK_DO_ARQUIVO_.github/workflows/ci.yml`

## 3. Pipeline implementado

O pipeline de CI executa:

1. leitura da configuracao do experimento;
2. instalacao de dependencias;
3. lint com Ruff;
4. testes automatizados com Pytest;
5. geracao de relatorios JUnit e JSON;
6. upload de artefatos;
7. execucao em modo paralelo ou sequencial.

O pipeline de CD executa um deploy simulado apos sucesso do CI e publica um
artefato contendo o resumo do deploy.

## 4. Hipotese inicial

Hipotese inicial:

> O uso de cache deve reduzir o tempo de instalacao de dependencias, o aumento
> da quantidade de testes deve elevar a duracao total do pipeline e a execucao
> paralela deve ser mais rapida que a sequencial quando lint e testes puderem
> rodar de forma independente.

## 5. Planejamento das execucoes

| Execucao | Variacao planejada | Resultado esperado |
|---|---|---|
| 1 | Baseline sem cache | Sucesso |
| 2 | Cache habilitado | Sucesso |
| 3 | Teste falhando propositalmente | Falha |
| 4 | Correcao do teste falhando | Sucesso |
| 5 | Aumento da quantidade de testes | Sucesso com maior duracao |
| 6 | Introducao de teste lento | Sucesso com aumento de duracao |
| 7 | Remocao do teste lento | Sucesso com reducao de duracao |
| 8 | Cache desabilitado | Sucesso com instalacao mais lenta |
| 9 | Cache habilitado novamente | Sucesso com possivel reducao |
| 10 | Jobs sequenciais | Sucesso com maior tempo total |
| 11 | Jobs paralelos | Sucesso com menor tempo total |
| 12 | Nova falha controlada | Falha |

## 6. Evidencias reais das execucoes

Preencher esta tabela apos as execucoes reais no GitHub Actions.

| Execucao | Run ID | Commit SHA | Mensagem do commit | Status | Variacao | Link |
|---|---|---|---|---|---|---|
| 1 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Baseline sem cache | `PREENCHER` |
| 2 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Cache habilitado | `PREENCHER` |
| 3 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Teste falhando | `PREENCHER` |
| 4 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Correcao da falha | `PREENCHER` |
| 5 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Mais testes | `PREENCHER` |
| 6 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Teste lento | `PREENCHER` |
| 7 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Sem teste lento | `PREENCHER` |
| 8 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Cache desabilitado | `PREENCHER` |
| 9 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Cache reabilitado | `PREENCHER` |
| 10 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Jobs sequenciais | `PREENCHER` |
| 11 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Jobs paralelos | `PREENCHER` |
| 12 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Nova falha controlada | `PREENCHER` |

## 7. Coleta de metricas

A coleta foi feita por script proprio em Python, localizado em
`scripts/collect_metrics.py`.

O script consulta a API do GitHub Actions, baixa os artefatos de teste e gera
uma base estruturada em CSV e JSON.

Base gerada:

- CSV: `metrics/pipeline_metrics.csv`
- JSON: `metrics/pipeline_metrics.json`

Campos principais coletados:

- `run_id`;
- `commit_sha`;
- `commit_message`;
- `status`;
- `workflow_duration`;
- `job_name`;
- `job_duration`;
- `step_name`;
- `step_duration`;
- `test_count`;
- `test_failures`;
- `average_test_time`;
- `timestamp`;
- `run_url`.

## 8. Graficos gerados

Inserir os graficos gerados apos a coleta:

![Tempo total do pipeline](charts/tempo-total-pipeline.png)

![Tempo por job](charts/tempo-por-job.png)

![Taxa de sucesso e falha](charts/taxa-sucesso-falha.png)

![Testes versus duracao](charts/testes-vs-duracao.png)

## 9. Analise dos resultados

### 9.1 Qual etapa mais contribuiu para o tempo total do pipeline?

`PREENCHER_APOS_ANALISE_DOS_DADOS`

### 9.2 Houve diferenca significativa entre execucoes com e sem cache?

`PREENCHER_APOS_ANALISE_DOS_DADOS`

### 9.3 O paralelismo reduziu o tempo total? Em que condicoes?

`PREENCHER_APOS_ANALISE_DOS_DADOS`

### 9.4 Quais falhas foram mais frequentes?

`PREENCHER_APOS_ANALISE_DOS_DADOS`

### 9.5 O pipeline fornece feedback rapido o suficiente para o desenvolvedor?

`PREENCHER_APOS_ANALISE_DOS_DADOS`

### 9.6 Que melhorias poderiam ser feitas no pipeline?

`PREENCHER_APOS_ANALISE_DOS_DADOS`

### 9.7 Quais limitacoes existem nos dados coletados?

`PREENCHER_APOS_ANALISE_DOS_DADOS`

### 9.8 Como essa analise poderia apoiar decisoes de engenharia?

`PREENCHER_APOS_ANALISE_DOS_DADOS`

## 10. Resultados inesperados

### Resultado inesperado 1

- Esperado: `PREENCHER`
- Observado: `PREENCHER`
- Evidencia nos dados: `PREENCHER`
- Possivel explicacao: `PREENCHER`

### Resultado inesperado 2

- Esperado: `PREENCHER`
- Observado: `PREENCHER`
- Evidencia nos dados: `PREENCHER`
- Possivel explicacao: `PREENCHER`

## 11. Comparacao entre hipotese inicial e resultado observado

`PREENCHER_APOS_ANALISE_DOS_DADOS`

## 12. Limitacoes do experimento

Possiveis limitacoes a discutir apos a coleta:

- amostra pequena, com apenas 12 execucoes;
- ambiente compartilhado e variavel do GitHub Actions;
- parte das falhas foi introduzida artificialmente;
- o projeto e pequeno e pode nao representar pipelines reais maiores;
- variacoes de rede podem afetar instalacao de dependencias;
- cache pode ter comportamento diferente entre cache frio e cache ja preenchido.

## 13. Melhorias propostas

Possiveis melhorias a avaliar apos a coleta:

- manter cache de dependencias habilitado;
- separar lint e testes para feedback mais rapido;
- rodar testes em paralelo quando a suite crescer;
- falhar cedo em lint antes de etapas mais caras, quando fizer sentido;
- monitorar tendencias de duracao ao longo do tempo;
- criar alertas para aumento anormal de tempo ou falhas recorrentes.

## 14. Como reproduzir

1. Clonar o repositorio.
2. Instalar as dependencias do projeto.
3. Fazer as 12 alteracoes planejadas em `experiment/variation.env`.
4. Criar um commit para cada variacao.
5. Enviar cada commit para o GitHub.
6. Aguardar as execucoes do GitHub Actions.
7. Rodar `scripts/collect_metrics.py`.
8. Rodar `scripts/generate_charts.py`.
9. Atualizar este relatorio com links, IDs, commits, graficos e analise.

