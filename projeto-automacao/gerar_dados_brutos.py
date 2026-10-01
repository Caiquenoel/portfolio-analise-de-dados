# -*- coding: utf-8 -*-
"""Gera um arquivo bruto e 'bagunçado' para simular o tipo de planilha que
chega na vida real (exportada de um sistema, preenchida por pessoas
diferentes, sem padronização) — ponto de partida do projeto de automação."""
import random
from datetime import date, timedelta
import openpyxl

random.seed(7)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Base"
ws.append(["Data", "Solicitante", "Categoria", "Descrição", "Valor", "Status"])

solicitantes = [" João Silva", "Maria Souza ", "Pedro Lima", " Ana Costa",
                "carlos alberto", "Fernanda Dias ", "J. Almeida", "  Rita Nunes"]

# variações "sujas" da mesma categoria
categorias = [
    "Material de Escritório", "material de escritório", "MATERIAL DE ESCRITÓRIO ",
    "Serviços Gráficos", "servicos graficos", "Serviços de TI", "SERVIÇOS DE TI",
    "Manutenção Predial", "manutenção predial ", "Viagens e Hospedagem",
    "viagens e hospedagem", "Limpeza e Higiene", "LIMPEZA E HIGIENE"
]

status_opts = ["Aprovado", "aprovado", "APROVADO", "Pendente", "pendente ",
               "Reprovado", "reprovado"]

descricoes = ["Compra de papel A4", "Impressão de banners", "Licença de software",
              "Reparo no ar-condicionado", "Passagem aérea", "Produtos de limpeza",
              "Cartuchos de impressora", "Manutenção de rede", "Hospedagem evento",
              "Toner para impressora"]

rows = []
start = date(2026, 1, 1)
for i in range(70):
    d = start + timedelta(days=random.randint(0, 240))
    # duas formatações de data diferentes (bagunça real comum)
    if random.random() < 0.5:
        data_str = d.strftime("%d/%m/%Y")
    else:
        data_str = d.strftime("%Y-%m-%d")

    solicitante = random.choice(solicitantes)
    categoria = random.choice(categorias)
    descricao = random.choice(descricoes)

    valor = round(random.uniform(50, 3200), 2)
    # três formatações de valor diferentes (bagunça real comum)
    r = random.random()
    if r < 0.4:
        valor_str = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    elif r < 0.7:
        valor_str = str(valor)
    else:
        valor_str = f" R${valor:.2f} "

    status = random.choice(status_opts)
    rows.append([data_str, solicitante, categoria, descricao, valor_str, status])

# injeta alguns valores faltando (realista)
for _ in range(5):
    idx = random.randint(0, len(rows) - 1)
    rows[idx][4] = None

# injeta algumas linhas duplicadas exatas (realista)
for _ in range(4):
    rows.append(random.choice(rows[:40]).copy())

random.shuffle(rows)

for row in rows:
    ws.append(row)

for col, w in zip("ABCDEF", [14, 18, 24, 26, 14, 14]):
    ws.column_dimensions[col].width = w

wb.save("/home/claude/solicitacoes_brutas.xlsx")
print("Arquivo bruto gerado com", len(rows), "linhas (incluindo duplicatas e valores faltando)")
