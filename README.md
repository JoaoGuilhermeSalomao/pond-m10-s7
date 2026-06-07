# Experimento de CI/CD com GitHub Actions

Este repositorio contem um projeto pequeno em Python criado para medir e
analisar execucoes reais de um pipeline CI/CD no GitHub Actions.

O projeto usado no experimento e uma biblioteca chamada `task_metrics`, que
calcula estatisticas simples de tarefas:

- total de tarefas;
- tarefas concluidas, pendentes e bloqueadas;
- percentual de conclusao;
- prioridade media;
- filtro por status;
- validacao de dados.

O foco da atividade nao e a complexidade da aplicacao, mas sim a instrumentacao
do pipeline, a coleta de metricas reais, a geracao de graficos e a analise
critica dos resultados.

## Estrutura

```text
.github/workflows/ci.yml       Pipeline de CI instrumentado
.github/workflows/cd.yml       Pipeline de CD simulado
src/                            Codigo da biblioteca
tests/                          Testes automatizados
scripts/collect_metrics.py      Coleta metricas pela API do GitHub
scripts/generate_charts.py      Gera os graficos obrigatorios
experiment/variation.env        Controla as variacoes entre execucoes
metrics/                        CSV/JSON gerados pelo script de coleta
charts/                         Graficos gerados
reports/                        Relatorios de teste locais
artifacts/                      Artefatos locais auxiliares
RELATORIO.md                    Relatorio tecnico do experimento
```

## O que o CI executa

O workflow `.github/workflows/ci.yml` executa:

1. leitura da configuracao do experimento;
2. instalacao de dependencias;
3. lint com Ruff;
4. testes automatizados com Pytest;
5. geracao de relatorios JUnit e JSON dos testes;
6. upload de artefatos;
7. execucao em modo paralelo ou sequencial, conforme a variacao.

O workflow `.github/workflows/cd.yml` executa um deploy simulado quando o CI
termina com sucesso, gerando um artefato de deploy.

## Configuracao das variacoes

As variacoes sao controladas pelo arquivo `experiment/variation.env`.

Campos principais:

```text
RUN_LABEL=run-01-baseline
CACHE_ENABLED=false
EXECUTION_MODE=parallel
TEST_CASES=8
SLOW_TEST_SECONDS=0
FORCE_TEST_FAILURE=false
```

Significado:

- `RUN_LABEL`: nome da execucao planejada;
- `CACHE_ENABLED`: ativa ou desativa cache de dependencias no workflow;
- `EXECUTION_MODE`: `parallel` ou `sequential`;
- `TEST_CASES`: quantidade de casos parametrizados gerados;
- `SLOW_TEST_SECONDS`: atraso artificial em um teste lento;
- `FORCE_TEST_FAILURE`: cria falha controlada quando definido como `true`.

## Plano minimo de 12 execucoes

Faca um commit para cada linha da tabela abaixo e envie para o GitHub. Cada push
gera uma execucao real do GitHub Actions.

| Execucao | RUN_LABEL | CACHE_ENABLED | EXECUTION_MODE | TEST_CASES | SLOW_TEST_SECONDS | FORCE_TEST_FAILURE | Objetivo |
|---|---|---|---|---:|---:|---|---|
| 1 | run-01-baseline | false | parallel | 8 | 0 | false | baseline sem cache |
| 2 | run-02-cache-on | true | parallel | 8 | 0 | false | medir cache inicial |
| 3 | run-03-failing-test | true | parallel | 8 | 0 | true | falha controlada |
| 4 | run-04-fix-test | true | parallel | 8 | 0 | false | correcao da falha |
| 5 | run-05-more-tests | true | parallel | 40 | 0 | false | aumentar volume de testes |
| 6 | run-06-slow-test | true | parallel | 40 | 3 | false | introduzir teste lento |
| 7 | run-07-remove-slow-test | true | parallel | 40 | 0 | false | remover lentidao artificial |
| 8 | run-08-cache-off | false | parallel | 40 | 0 | false | comparar sem cache |
| 9 | run-09-cache-on-again | true | parallel | 40 | 0 | false | comparar com cache preenchido |
| 10 | run-10-sequential | true | sequential | 40 | 0 | false | medir jobs sequenciais |
| 11 | run-11-parallel | true | parallel | 40 | 0 | false | medir jobs paralelos |
| 12 | run-12-failing-test-again | true | parallel | 40 | 0 | true | segunda falha controlada |

Exemplo de mensagem de commit:

```text
run 05: increase generated test cases
```

## Coleta das metricas

Depois que as 12 execucoes reais terminarem, gere um token do GitHub com acesso
de leitura ao repositorio e execute:

```bash
export GITHUB_TOKEN=seu_token
python scripts/collect_metrics.py \
  --repo JoaoGuilhermeSalomao/pond-m10-s7 \
  --workflow ci.yml \
  --limit 20 \
  --out metrics/pipeline_metrics.csv \
  --json-out metrics/pipeline_metrics.json
```

O CSV gerado contem, entre outros campos:

```text
run_id,commit_sha,commit_message,status,workflow_duration,job_name,job_duration,step_name,step_duration,test_count,test_failures,average_test_time,timestamp
```

## Geracao dos graficos

Com o CSV gerado, execute:

```bash
python scripts/generate_charts.py \
  --input metrics/pipeline_metrics.csv \
  --out-dir charts
```

O script gera os quatro graficos obrigatorios:

- `charts/tempo-total-pipeline.png`;
- `charts/tempo-por-job.png`;
- `charts/taxa-sucesso-falha.png`;
- `charts/testes-vs-duracao.png`.

## Execucao local

Para validar localmente:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ruff check .
python -m pytest
```

## Entregaveis

Os entregaveis finais tambem foram centralizados em `entregaveis/`.

Ao final do experimento, entregue:

- link do repositorio GitHub;
- link do arquivo `.github/workflows/ci.yml`;
- script `scripts/collect_metrics.py`;
- base `metrics/pipeline_metrics.csv` ou `metrics/pipeline_metrics.json`;
- graficos em `charts/`;
- relatorio `RELATORIO.md`;
- links ou prints das execucoes reais do GitHub Actions;
- IDs reais das execucoes;
- commits reais usados;
- explicacao das variacoes realizadas.
