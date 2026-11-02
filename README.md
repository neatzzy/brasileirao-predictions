# Brasileirão Predictions

Um projeto de análise de dados e treinamento de modelo para prever resultados de partidas do Campeonato Brasileiro de Futebol.

O objetivo é prever se o **time mandante vai vencer, empatar ou perder** a próxima partida, usando Random Forest e XGBoost sobre estatísticas das partidas anteriores (gols, finalizações, posse, mando de campo e forma nos últimos 5 jogos), com uma interface web em Streamlit para visualizar os resultados.

## Dados

Os dados foram baixados do **Kaggle** em **02/11/2026** e ficam em `data/raw/` (descritos em `data/raw/Legenda.txt`):

| Arquivo | Conteúdo |
| --- | --- |
| `campeonato-brasileiro-full.csv` | uma linha por partida (rodada, data, times, placar, técnicos, arena...) |
| `campeonato-brasileiro-estatisticas-full.csv` | estatísticas por clube em cada partida (chutes, posse, passes, faltas...) |
| `campeonato-brasileiro-gols.csv` | um gol por linha |
| `campeonato-brasileiro-cartoes.csv` | um cartão por linha |

Cobertura: partidas de 2003 até 2025-12-07. Chutes e posse só existem a partir de 2015, e a temporada de 2024 não tem estatísticas. Os detalhes estão na seção "Dados disponíveis" do plano.

Os arquivos originais não devem ser editados à mão; o resultado do processamento vai para `data/processed/`.

## Como rodar

O projeto usa o [uv](https://docs.astral.sh/uv/) e Python 3.14.

```shell
uv sync                           # cria o .venv e instala as dependências
uv run pytest                     # testes
uv run jupyter lab                # notebooks
uv run streamlit run app/Home.py  # interface web (quando existir)
```

Para adicionar uma biblioteca, use `uv add <pacote>` (ou `uv add --dev <pacote>` para ferramentas de desenvolvimento).

## Estrutura

```text
data/raw/        # CSVs originais do Kaggle + Legenda.txt
data/processed/  # dados limpos e com features
src/brasileirao_predictions/  # código do projeto (pacote instalável)
app/             # interface web (Streamlit)
notebooks/       # exploração
reports/figures/ # gráficos gerados
models/          # modelos treinados
tests/           # testes
plan/PLANO.md    # plano de desenvolvimento
```

## Status

Em planejamento: o ambiente está configurado e o plano está escrito; o código ainda não foi implementado.
