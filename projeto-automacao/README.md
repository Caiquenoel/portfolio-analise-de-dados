# Automação de Relatório — Solicitações de Compra

Projeto de portfólio — Caíque Augusto Rufino Noel

## Objetivo

Demonstrar automação de uma tarefa administrativa recorrente: transformar uma planilha bruta, bagunçada e sem padronização em um relatório gerencial limpo, formatado e pronto para leitura — com um clique, em vez de horas de trabalho manual.

## O problema que o script resolve

Planilhas recebidas de sistemas ou preenchidas por várias pessoas normalmente vêm com:
- Datas em formatos diferentes (`15/03/2026` e `2026-03-15` misturados)
- Valores como texto, com "R$", separador de milhar e vírgula decimal
- A mesma categoria escrita de formas diferentes (`Material de Escritório`, `material de escritório`, `MATERIAL DE ESCRITÓRIO `)
- Linhas duplicadas
- Campos em branco

Tratar isso manualmente, todo mês, é repetitivo e sujeito a erro. O script `automatiza_relatorio.py` faz esse tratamento inteiro de forma automática e sempre igual.

## O que o script faz

1. **Lê** o arquivo bruto (`solicitacoes_brutas.xlsx`)
2. **Diagnostica** a qualidade do dado antes de tratar (conta duplicatas, valores faltando, variações de texto)
3. **Limpa**: remove duplicatas, padroniza texto (categoria e status), converte datas e valores para os tipos corretos
4. **Sinaliza** (em vez de descartar) solicitações com valor faltando, para revisão manual
5. **Agrega** os dados por categoria, status e mês
6. **Gera** um relatório Excel formatado com 3 abas: Sobre e Log de Tratamento, Dados Tratados, e Resumo com KPIs e gráficos

## Resultado (nesta execução de exemplo)

- Arquivo bruto: 74 linhas, 13 variações de categoria, 7 variações de status
- Depois do tratamento: 70 linhas válidas, 6 categorias padronizadas, 3 status padronizados
- 4 duplicatas removidas automaticamente
- 4 solicitações sinalizadas para revisão (valor ausente no arquivo original) — sem serem descartadas silenciosamente

## Estrutura do projeto

```
├── gerar_dados_brutos.py              # gera o arquivo de exemplo "bagunçado" (simula o problema real)
├── automatiza_relatorio.py            # o script de automação em si
├── solicitacoes_brutas.xlsx           # entrada bruta de exemplo
├── solicitacoes_tratadas.csv          # saída intermediária já limpa
├── Relatorio_Solicitacoes_Compra.xlsx # relatório final formatado
└── README.md
```

## Como executar

```bash
pip install pandas openpyxl
python automatiza_relatorio.py
```

O script pode ser reaproveitado para qualquer planilha no mesmo formato — basta apontar para um novo arquivo de entrada, sem precisar repetir o trabalho manual de limpeza.
