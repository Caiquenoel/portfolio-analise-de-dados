# -*- coding: utf-8 -*-
"""
Análise de Eficiência de Produção — Python + SQL
Projeto de portfólio — Caíque Augusto Rufino Noel

Carrega os dados de produção em um banco SQLite, executa consultas SQL
para responder perguntas de negócio, e gera visualizações com os
resultados.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

NAVY = "#1a3d5c"
RED = "#c62828"
GREEN = "#2e7d32"
GREY = "#888888"

# ---------------------------------------------------------------------
# 1. Carregar CSV e criar banco de dados SQLite
# ---------------------------------------------------------------------
df = pd.read_csv("dados_producao_poweBI.csv", sep=";", encoding="utf-8-sig")
df.columns = ["data", "linha", "turno", "meta", "produzido", "refugo", "parada_min", "responsavel"]
df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
df["mes"] = df["data"].dt.to_period("M").astype(str)

conn = sqlite3.connect(":memory:")
df.to_sql("producao", conn, index=False, if_exists="replace")

print("Banco de dados criado com", len(df), "registros.\n")

# ---------------------------------------------------------------------
# 2. Consultas SQL — cada uma respondendo uma pergunta de negócio
# ---------------------------------------------------------------------

# Q1: Qual linha tem o melhor atingimento de meta?
q1 = """
SELECT
    linha,
    SUM(meta) AS meta_total,
    SUM(produzido) AS produzido_total,
    ROUND(100.0 * SUM(produzido) / SUM(meta), 1) AS atingimento_pct,
    ROUND(100.0 * SUM(refugo) / SUM(produzido), 2) AS taxa_refugo_pct
FROM producao
GROUP BY linha
ORDER BY atingimento_pct DESC;
"""
q1_df = pd.read_sql(q1, conn)
print("=== Atingimento de meta e refugo por linha ===")
print(q1_df.to_string(index=False), "\n")

# Q2: Como evoluiu o atingimento de meta mês a mês?
q2 = """
SELECT
    mes,
    SUM(meta) AS meta_total,
    SUM(produzido) AS produzido_total,
    ROUND(100.0 * SUM(produzido) / SUM(meta), 1) AS atingimento_pct
FROM producao
GROUP BY mes
ORDER BY mes;
"""
q2_df = pd.read_sql(q2, conn)
print("=== Evolução mensal do atingimento de meta ===")
print(q2_df.to_string(index=False), "\n")

# Q3: Existe relação entre tempo de parada e taxa de refugo? (por linha/dia)
q3 = """
SELECT
    linha,
    turno,
    ROUND(AVG(parada_min), 1) AS parada_media_min,
    ROUND(100.0 * SUM(refugo) / SUM(produzido), 2) AS taxa_refugo_pct,
    COUNT(*) AS n_registros
FROM producao
GROUP BY linha, turno
ORDER BY linha, turno;
"""
q3_df = pd.read_sql(q3, conn)
print("=== Parada média e taxa de refugo por linha e turno ===")
print(q3_df.to_string(index=False), "\n")

# Q4: Ranking de responsáveis por produtividade média (produzido/meta)
q4 = """
SELECT
    responsavel,
    COUNT(*) AS dias_registrados,
    ROUND(100.0 * SUM(produzido) / SUM(meta), 1) AS atingimento_medio_pct
FROM producao
GROUP BY responsavel
ORDER BY atingimento_medio_pct DESC;
"""
q4_df = pd.read_sql(q4, conn)
print("=== Ranking de atingimento médio por responsável ===")
print(q4_df.to_string(index=False), "\n")

conn.close()

# ---------------------------------------------------------------------
# 3. Visualizações
# ---------------------------------------------------------------------

# Gráfico 1: Atingimento de meta por linha
fig, ax = plt.subplots(figsize=(7, 4.2))
bars = ax.bar(q1_df["linha"], q1_df["atingimento_pct"], color=NAVY, width=0.5)
ax.axhline(100, color=RED, linestyle="--", linewidth=1, label="Meta (100%)")
for b in bars:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1, f"{b.get_height():.1f}%",
            ha="center", fontsize=10, color=NAVY, fontweight="bold")
ax.set_title("Atingimento de Meta por Linha de Produção", fontsize=13, fontweight="bold", color=NAVY)
ax.set_ylabel("% Atingimento")
ax.set_ylim(0, max(q1_df["atingimento_pct"].max() + 10, 110))
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig("grafico_atingimento_por_linha.png", dpi=150)
plt.close()

# Gráfico 2: Evolução mensal do atingimento
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.plot(q2_df["mes"], q2_df["atingimento_pct"], marker="o", color=NAVY, linewidth=2)
for x, y in zip(q2_df["mes"], q2_df["atingimento_pct"]):
    ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points", xytext=(0, 8),
                ha="center", fontsize=9, color=NAVY)
ax.axhline(100, color=RED, linestyle="--", linewidth=1, label="Meta (100%)")
ax.set_title("Evolução do Atingimento de Meta (1º Trimestre 2026)", fontsize=13, fontweight="bold", color=NAVY)
ax.set_ylabel("% Atingimento")
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig("grafico_evolucao_mensal.png", dpi=150)
plt.close()

# Gráfico 3: Taxa de refugo por linha e turno (heatmap simples com barras agrupadas)
pivot = q3_df.pivot(index="linha", columns="turno", values="taxa_refugo_pct")
fig, ax = plt.subplots(figsize=(7, 4.2))
pivot.plot(kind="bar", ax=ax, color=[NAVY, "#4a7ba6", "#a8c4de"])
ax.set_title("Taxa de Refugo por Linha e Turno", fontsize=13, fontweight="bold", color=NAVY)
ax.set_ylabel("Taxa de Refugo (%)")
ax.set_xlabel("")
ax.tick_params(axis="x", rotation=0)
ax.legend(title="Turno", frameon=False)
plt.tight_layout()
plt.savefig("grafico_refugo_linha_turno.png", dpi=150)
plt.close()

print("Gráficos salvos: grafico_atingimento_por_linha.png, grafico_evolucao_mensal.png, "
      "grafico_refugo_linha_turno.png")
