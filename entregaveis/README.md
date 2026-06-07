# Entregaveis da Atividade CI/CD

Esta pasta centraliza os entregaveis solicitados na atividade. Alguns arquivos
tambem permanecem em seus locais originais porque precisam estar la para o
projeto funcionar corretamente.

## 1. Link do repositorio GitHub

Repositorio:

- <https://github.com/JoaoGuilhermeSalomao/pond-m10-s7>

## 2. Link do arquivo YAML do GitHub Actions

Arquivo YAML principal do CI:

- <https://github.com/JoaoGuilhermeSalomao/pond-m10-s7/blob/main/.github/workflows/ci.yml>

Arquivo YAML do CD simulado:

- <https://github.com/JoaoGuilhermeSalomao/pond-m10-s7/blob/main/.github/workflows/cd.yml>

Observacao importante: os workflows precisam permanecer em `.github/workflows/`,
pois esse e o caminho obrigatorio para o GitHub Actions reconhecer e executar
os pipelines. Copias de consulta tambem foram colocadas em:

- `entregaveis/workflows/ci.yml`
- `entregaveis/workflows/cd.yml`

## 3. Script de coleta das metricas

Script principal:

- `entregaveis/scripts/collect_metrics.py`

Local original no projeto:

- `scripts/collect_metrics.py`

## 4. Base de dados gerada em CSV ou JSON

Bases geradas a partir de execucoes reais do GitHub Actions:

- `entregaveis/metrics/pipeline_metrics.csv`
- `entregaveis/metrics/pipeline_metrics.json`

Locais originais no projeto:

- `metrics/pipeline_metrics.csv`
- `metrics/pipeline_metrics.json`

## 5. Graficos produzidos

Graficos obrigatorios:

- `entregaveis/charts/tempo-total-pipeline.png`
- `entregaveis/charts/tempo-por-job.png`
- `entregaveis/charts/taxa-sucesso-falha.png`
- `entregaveis/charts/testes-vs-duracao.png`

Os graficos correspondem a:

- tempo total do pipeline por execucao;
- tempo por job;
- taxa de sucesso e falha;
- relacao entre quantidade de testes e duracao do pipeline.

## 6. Relatorio tecnico em Markdown

Relatorio final:

- `entregaveis/RELATORIO.md`

Local original no projeto:

- `RELATORIO.md`

O relatorio contem:

- links das execucoes reais;
- IDs reais dos workflows executados;
- commits reais usados no experimento;
- explicacao das variacoes realizadas;
- graficos gerados a partir dos dados coletados;
- analise de resultados inesperados;
- comparacao entre hipotese inicial e resultado observado;
- limitacoes do experimento.

## 7. Breve explicacao sobre como reproduzir o experimento

Para reproduzir:

1. Clone o repositorio.
2. Instale as dependencias com `python -m pip install -r requirements.txt`.
3. Altere `experiment/variation.env` conforme o plano de variacoes descrito no
   `README.md` da raiz.
4. Crie um commit para cada variacao.
5. Envie os commits para o GitHub para disparar o GitHub Actions.
6. Aguarde as execucoes terminarem.
7. Execute `scripts/collect_metrics.py` para gerar CSV/JSON.
8. Execute `scripts/generate_charts.py` para gerar os graficos.
9. Atualize ou consulte `RELATORIO.md` com as evidencias reais.

## 8. Conferencia dos requisitos

| Requisito | Onde esta |
|---|---|
| Link do repositorio GitHub | Este arquivo, secao 1 |
| Link do YAML do GitHub Actions | Este arquivo, secao 2 |
| Script de coleta das metricas | `entregaveis/scripts/collect_metrics.py` |
| Base CSV/JSON | `entregaveis/metrics/` |
| Graficos produzidos | `entregaveis/charts/` |
| Relatorio tecnico em Markdown | `entregaveis/RELATORIO.md` |
| Explicacao de reproducao | Este arquivo, secao 7 |

