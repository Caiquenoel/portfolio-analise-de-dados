# Análise de Dados Públicos — Cotação do Dólar (USD/BRL)

Projeto de portfólio — Caíque Augusto Rufino Noel

## Objetivo

Demonstrar a capacidade de trabalhar com **dado público real** (não fictício) — buscando diretamente na API oficial, tratando o formato bruto e extraindo insights de negócio, com aplicação prática para áreas administrativas/financeiras (ex.: apoio a decisões de importação, compras internacionais, ou análise de risco cambial).

## Fonte dos dados

**Banco Central do Brasil — Sistema Gerenciador de Séries Temporais (SGS), série nº 1** (Taxa de câmbio livre — Dólar americano, venda, diária). Dados públicos e oficiais, obtidos diretamente da API: `api.bcb.gov.br`.

Período analisado: janeiro/2010 a dezembro/2016 (1.760 registros diários).

## Tratamento aplicado ao dado bruto

A API retorna os dados como texto simples (datas e valores em formato string), sem nenhum tratamento — etapas aplicadas:

- Conversão de datas de texto (`dd/mm/aaaa`) para formato de data
- Conversão dos valores de texto para número decimal
- Verificação e remoção de duplicidades
- Ordenação cronológica
- Agregação mensal e anual para permitir análise de tendência (a ausência de cotação em fins de semana/feriados é uma característica do mercado, não um erro de dado — por isso a análise usa agregações que absorvem isso naturalmente)

## Perguntas de negócio respondidas

1. Em qual mês o dólar teve a maior alta e a maior queda no período?
2. Qual ano apresentou a maior volatilidade cambial?
3. Como evoluiu a cotação média ano a ano?

## Principais insights

- O período de **2015 foi o de maior volatilidade** do câmbio (desvio padrão diário de R$ 0,43, mais de 3x a volatilidade média dos anos anteriores) — coincide com a crise econômica e política brasileira daquele ano.
- A maior alta mensal ocorreu em **março/2015 (+11,5%)**, e a maior queda em **março/2016 (-6,8%)** — ambos momentos de forte instabilidade política.
- A cotação média saltou de **R$ 1,76 em 2010 para R$ 3,48 em 2016** — uma desvalorização acumulada do real de quase 100% frente ao dólar no período.
- Para uma área administrativa/financeira, esse tipo de análise apoiaria decisões como: melhor momento para negociar contratos em dólar, dimensionamento de reservas cambiais, ou análise de risco em compras internacionais.

## Estrutura do projeto

```
├── analise_cambio.py                  # script principal (tratamento + análise + gráficos)
├── cambio_raw.json                    # dado bruto, exatamente como veio da API do BCB
├── cambio_usd_brl_tratado.csv         # dado já limpo e tratado
├── grafico_serie_completa.png
├── grafico_volatilidade_anual.png
├── grafico_media_anual.png
└── README.md
```

## Como executar

```bash
pip install pandas matplotlib
python analise_cambio.py
```

## Fonte oficial

Dados obtidos via API pública do Banco Central do Brasil:
`https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json`
