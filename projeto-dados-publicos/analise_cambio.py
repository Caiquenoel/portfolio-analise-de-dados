# -*- coding: utf-8 -*-
"""
Análise de Dados Públicos — Cotação do Dólar (USD/BRL)
Fonte: Banco Central do Brasil, sistema SGS, série 1 (dados abertos, oficiais)
Projeto de portfólio — Caíque Augusto Rufino Noel
"""

import json
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

NAVY = "#1a3d5c"
RED = "#c62828"

# ---------------------------------------------------------------------
# 1. Carregar dado bruto (exatamente como veio da API do Banco Central)
# ---------------------------------------------------------------------
with open("cambio_raw.json", encoding="utf-8") as f:
    raw = json.load(f)

df = pd.DataFrame(raw)
print("Registros brutos recebidos da API:", len(df))
print(df.head(3), "\n")

# ---------------------------------------------------------------------
# 2. Tratamento (o dado bruto vem como texto, precisa virar data/número)
# ---------------------------------------------------------------------
df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
df["valor"] = df["valor"].astype(float)
df = df.sort_values("data").drop_duplicates(subset="data").reset_index(drop=True)

print("Período coberto:", df["data"].min().date(), "a", df["data"].max().date())
print("Registros após limpeza:", len(df), "\n")

# Cotação só existe em dia útil (não é dado faltando, é característica real
# do mercado) — por isso a análise usa agregação mensal, que já lida com isso.
df["ano_mes"] = df["data"].dt.to_period("M")

mensal = df.groupby("ano_mes")["valor"].agg(["mean", "std", "min", "max"]).reset_index()
mensal["ano_mes_str"] = mensal["ano_mes"].astype(str)
mensal["variacao_mensal_pct"] = mensal["mean"].pct_change() * 100

# ---------------------------------------------------------------------
# 3. Perguntas de negócio
# ---------------------------------------------------------------------

# Q1: Qual foi o pior e o melhor mês (maior alta e maior queda)?
pior_mes = mensal.loc[mensal["variacao_mensal_pct"].idxmax()]
melhor_mes = mensal.loc[mensal["variacao_mensal_pct"].idxmin()]
print(f"Maior alta mensal: {pior_mes['ano_mes_str']} ({pior_mes['variacao_mensal_pct']:.1f}%)")
print(f"Maior queda mensal: {melhor_mes['ano_mes_str']} ({melhor_mes['variacao_mensal_pct']:.1f}%)\n")

# Q2: Qual ano teve a maior volatilidade média (desvio padrão diário)?
df["ano"] = df["data"].dt.year
vol_ano = df.groupby("ano")["valor"].std().reset_index(name="volatilidade")
print("=== Volatilidade (desvio padrão) por ano ===")
print(vol_ano.to_string(index=False), "\n")

# Q3: Comparação da média anual (visão de tendência de longo prazo)
media_ano = df.groupby("ano")["valor"].mean().reset_index(name="media_cambio")
print("=== Cotação média por ano ===")
print(media_ano.to_string(index=False), "\n")

# ---------------------------------------------------------------------
# 4. Visualizações
# ---------------------------------------------------------------------

# Gráfico 1: série completa com destaque no período de maior volatilidade
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(df["data"], df["valor"], color=NAVY, linewidth=1.2)
ano_mais_volatil = int(vol_ano.loc[vol_ano["volatilidade"].idxmax(), "ano"])
periodo = df[df["ano"] == ano_mais_volatil]
ax.axvspan(periodo["data"].min(), periodo["data"].max(), color=RED, alpha=0.12,
           label=f"Ano de maior volatilidade ({ano_mais_volatil})")
ax.set_title("Cotação do Dólar (USD/BRL) — 2010 a 2016", fontsize=13, fontweight="bold", color=NAVY)
ax.set_ylabel("R\$ por US\$")
ax.legend(frameon=False, loc="upper left")
plt.tight_layout()
plt.savefig("grafico_serie_completa.png", dpi=150)
plt.close()

# Gráfico 2: volatilidade por ano
fig, ax = plt.subplots(figsize=(7, 4.2))
bars = ax.bar(vol_ano["ano"].astype(str), vol_ano["volatilidade"], color=NAVY)
bars[list(vol_ano["ano"]).index(ano_mais_volatil)].set_color(RED)
ax.set_title("Volatilidade do Câmbio por Ano (desvio padrão diário)", fontsize=13,
              fontweight="bold", color=NAVY)
ax.set_ylabel("Desvio padrão (R\\$)")
plt.tight_layout()
plt.savefig("grafico_volatilidade_anual.png", dpi=150)
plt.close()

# Gráfico 3: média anual (tendência)
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.plot(media_ano["ano"], media_ano["media_cambio"], marker="o", color=NAVY, linewidth=2)
for x, y in zip(media_ano["ano"], media_ano["media_cambio"]):
    ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(0, 8),
                ha="center", fontsize=9, color=NAVY)
ax.set_title("Cotação Média Anual do Dólar (USD/BRL)", fontsize=13, fontweight="bold", color=NAVY)
ax.set_ylabel("R\$ por US\$")
ax.set_xticks(media_ano["ano"])
plt.tight_layout()
plt.savefig("grafico_media_anual.png", dpi=150)
plt.close()

# Salvar dado tratado (evidência do processo de limpeza)
df[["data", "valor"]].to_csv("cambio_usd_brl_tratado.csv", index=False, sep=";")

print("Gráficos salvos: grafico_serie_completa.png, grafico_volatilidade_anual.png, "
      "grafico_media_anual.png")
print("Dado tratado salvo em: cambio_usd_brl_tratado.csv")
