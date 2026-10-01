# Análise de Eficiência de Produção — Python + SQL

Projeto de portfólio — Caíque Augusto Rufino Noel

## Objetivo

Demonstrar aplicação prática de **SQL** e **Python** para análise de dados operacionais, respondendo perguntas de negócio reais sobre eficiência de produção — mesmo tipo de rotina de controle de processos e indicadores da minha experiência profissional.

## Contexto

Simula o acompanhamento diário de 3 linhas de produção ao longo de um trimestre (231 registros), com meta, produção realizada, refugo, paradas de linha, turno e responsável.

## Ferramentas utilizadas

- **Python** (pandas, matplotlib)
- **SQL** (SQLite, via `sqlite3`)

## Perguntas de negócio respondidas

1. Qual linha de produção tem o melhor atingimento de meta e a menor taxa de refugo?
2. Como evoluiu o atingimento de meta ao longo do trimestre?
3. Existe diferença na taxa de refugo entre turnos, dentro de cada linha?
4. Qual responsável tem o melhor desempenho médio de atingimento de meta?

## Principais insights

- Todas as 3 linhas ficaram abaixo da meta (91–93%), com a **Linha C** apresentando o melhor atingimento (92,9%) e a menor taxa de refugo (3,41%).
- O atingimento de meta **melhorou mês a mês** ao longo do trimestre (91,2% → 92,6% → 93,5%), sugerindo uma curva de aprendizado ou ajuste operacional.
- A taxa de refugo varia por turno dentro de cada linha — por exemplo, a Linha A tem maior refugo no turno da tarde, o que pode indicar oportunidade de investigação pontual (fadiga da equipe, manutenção, etc.).
- Há variação de desempenho entre responsáveis (90,5% a 94,0% de atingimento médio), o que pode orientar ações de treinamento ou benchmarking interno.

## Estrutura do projeto

```
├── analise_producao.py                  # script principal (consultas SQL + gráficos)
├── dados_producao_poweBI.csv            # base de dados utilizada
├── grafico_atingimento_por_linha.png
├── grafico_evolucao_mensal.png
├── grafico_refugo_linha_turno.png
└── README.md
```

## Como executar

```bash
pip install pandas matplotlib
python analise_producao.py
```

---
*Dados fictícios, gerados para fins de demonstração deste portfólio.*
