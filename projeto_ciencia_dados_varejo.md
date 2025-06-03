# Projeto de Ciência de Dados: Análise de Vendas e Segmentação de Clientes no Varejo

**Autor:** Willian
**Data:** 03 de Junho de 2025
**Tecnologias:** Python (Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn), SQL (SQLite)

## Resumo Executivo

Este projeto demonstra um fluxo completo de ciência de dados aplicado a um cenário de vendas no varejo. Utilizando um dataset sintético, realizamos desde a definição do problema de negócio, passando pela geração e tratamento dos dados, análise exploratória (EDA), até a construção de um modelo de segmentação de clientes baseado em RFM (Recência, Frequência, Valor Monetário) e K-Means. O objetivo é fornecer insights acionáveis sobre o comportamento do consumidor e o desempenho das vendas, utilizando Python e SQL como ferramentas principais. Todo o processo foi documentado visando clareza e replicabilidade, ideal para compor um portfólio de ciência de dados.

---



# Projeto de Ciência de Dados: Análise de Vendas no Varejo

## 1. Problema de Negócio

Uma empresa de varejo busca otimizar suas operações e estratégias de marketing através de uma compreensão mais profunda dos seus dados de vendas. A falta de uma análise sistemática impede a identificação de padrões chave, oportunidades de crescimento e a personalização da experiência do cliente. Questões como quais produtos impulsionam as vendas, quem são os clientes mais valiosos e como as vendas flutuam ao longo do tempo precisam ser respondidas com base em dados concretos.

## 2. Objetivos do Projeto

Este projeto visa analisar dados históricos de vendas para extrair insights acionáveis. Os objetivos específicos são:

*   **Analisar o Desempenho de Produtos:** Identificar os produtos e categorias com maior volume de vendas e receita. Analisar a contribuição de cada categoria para o faturamento total.
*   **Analisar Tendências Temporais:** Investigar padrões de vendas ao longo do tempo (diário, semanal, mensal) para entender sazonalidades e picos de demanda.
*   **Segmentar Clientes:** Agrupar clientes com base em seu comportamento de compra (ex: frequência, valor gasto total, recência da última compra - Análise RFM) para identificar segmentos de alto valor e direcionar ações de marketing.
*   **Explorar Relações:** Investigar possíveis correlações entre produtos (quais produtos são frequentemente comprados juntos).
*   **(Opcional/Avançado) Previsão de Vendas:** Desenvolver um modelo simples para prever as vendas de uma categoria ou produto específico para as próximas semanas/mês.

## 3. Tecnologias Utilizadas

*   **Linguagem de Programação:** Python (com bibliotecas como Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn)
*   **Banco de Dados:** SQL (para consulta, agregação e extração inicial de dados)

Este projeto fornecerá uma base sólida para a tomada de decisões estratégicas na empresa, utilizando técnicas de ciência de dados para transformar dados brutos em inteligência de negócio.





## 4. Metodologia

O projeto seguiu um fluxo padrão de ciência de dados, detalhado nas seções seguintes.

### 4.1. Geração e Preparação dos Dados

Conforme descrito no plano inicial (`02_data_plan.md`), optou-se por gerar um dataset sintético para garantir controle e replicabilidade. O script `generate_data.py` foi utilizado para criar 50.000 registros de vendas simuladas, abrangendo o período de 2023 a 2024, com informações de pedidos, clientes, produtos, categorias, valores, regiões e métodos de pagamento. Uma pequena porcentagem de dados faltantes foi introduzida propositalmente em `CustomerID` e `Region` para simular um cenário mais realista.

```python
# Trecho de generate_data.py - Geração de Dados
# ... (código para definir categorias, produtos, preços)

data = []
order_id_counter = 1
date_range = (end_date - start_date).days

for i in range(num_records):
    # ... (lógica para gerar dados aleatórios para cada coluna)

    # Adiciona um pouco de dados faltantes
    if random.random() < 0.01:
        customer_id_final = np.nan
    else:
        customer_id_final = customer_id
    if random.random() < 0.005:
        region_final = np.nan
    else:
        region_final = region

    data.append({ # Dicionário com os dados da linha })
    order_id_counter += 1

df = pd.DataFrame(data)
df["CustomerID"] = df["CustomerID"].astype("Int64") # Permite NaNs para inteiros
df.to_csv("/home/ubuntu/online_sales_raw.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")
```

O dataset bruto (`online_sales_raw.csv`) foi então processado pelo script `eda_analysis.py`. As etapas de limpeza incluíram:

*   **Carregamento dos Dados:** Leitura do CSV para um DataFrame Pandas, com parsing automático da coluna `Date`.
*   **Tratamento de Nulos:**
    *   As linhas com `Region` nula foram removidas (representavam uma pequena fração do dataset).
    *   Os `CustomerID` nulos foram preenchidos com `-1` e a coluna convertida para `int`, para facilitar análises futuras onde um ID é necessário (embora para a segmentação RFM/K-Means, esses clientes foram posteriormente filtrados).
*   **Verificação de Duplicatas:** Nenhuma linha duplicada foi encontrada.
*   **Conversão de Tipos:** Verificação e ajuste dos tipos de dados (ex: `Date` para datetime, numéricos para float/int).
*   **Engenharia de Atributos:** Criação de novas colunas derivadas da data (`Year`, `Month`, `Week`, `DayOfWeek`, `Hour`, `DateOnly`) para facilitar análises temporais.

```python
# Trecho de eda_analysis.py - Limpeza e Pré-processamento

df = pd.read_csv(raw_data_path, parse_dates=["Date"])

# Tratamento de Nulos
initial_rows = len(df)
df["CustomerID"] = df["CustomerID"].fillna(-1).astype(int)
df.dropna(subset=["Region"], inplace=True)

# Engenharia de Atributos
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
# ... (outras colunas de data)

# Salvar dados processados
df.to_csv(processed_data_path, index=False, date_format="%Y-%m-%d %H:%M:%S")

# Opcional: Carregar no SQLite
conn = sqlite3.connect(db_path)
df.to_sql("sales_processed", conn, if_exists="replace", index=False)
conn.close()
```

Os dados processados foram salvos em `online_sales_processed.csv` e também carregados em uma tabela `sales_processed` no banco de dados SQLite (`sales_database.db`) para demonstrar a integração com SQL.

---



### 4.2. Análise Exploratória de Dados (EDA)

A Análise Exploratória de Dados foi realizada no script `eda_analysis.py` utilizando os dados processados. O objetivo foi obter uma compreensão inicial dos padrões e tendências presentes nos dados de vendas. As principais análises incluíram:

*   **Estatísticas Descritivas:** Análise das métricas centrais (média, mediana, quartis) e de dispersão (desvio padrão, mínimo, máximo) para as colunas numéricas (`Quantity`, `UnitPrice`, `TotalPrice`).
*   **Distribuição de Variáveis Numéricas:** Histogramas foram gerados para visualizar a distribuição das quantidades, preços unitários e totais (ver `01_numeric_distributions.png`). Observou-se uma concentração de vendas em quantidades e preços menores, com uma cauda longa indicando vendas de maior valor, porém menos frequentes.
*   **Vendas ao Longo do Tempo:** Um gráfico de linha mostrou a tendência das vendas totais mensais ao longo dos dois anos (ver `02_monthly_sales_trend.png`), permitindo identificar possíveis sazonalidades ou crescimento.
*   **Vendas por Categoria e Região:** Gráficos de barras compararam o desempenho de vendas entre diferentes categorias de produtos (ver `03_sales_by_category.png`) e regiões geográficas (ver `04_sales_by_region.png`), destacando as áreas de maior contribuição para a receita.
*   **Top Produtos:** Identificação dos 10 produtos mais vendidos, tanto em termos de quantidade quanto de receita gerada (ver `05_top_10_products.png`), revelando os itens chave do catálogo.
*   **Padrões Temporais Detalhados:** Análise das vendas por dia da semana (ver `06_sales_by_dayofweek.png`) e por hora do dia (ver `07_sales_by_hour.png`) para identificar picos de atividade comercial.
*   **Métodos de Pagamento:** Um gráfico de pizza ilustrou a popularidade dos diferentes métodos de pagamento utilizados pelos clientes (ver `08_payment_method_distribution.png`).

```python
# Trecho de eda_analysis.py - Exemplo de Análise (Vendas por Categoria)

category_sales = df.groupby('Category')['TotalPrice'].sum().sort_values(ascending=False)
fig = plt.figure()
sns.barplot(x=category_sales.values, y=category_sales.index, palette='viridis')
plt.title('Vendas Totais por Categoria')
plt.xlabel('Vendas Totais')
plt.ylabel('Categoria')
save_plot('03_sales_by_category.png', fig)
```

Os insights gerados nesta fase forneceram uma base sólida para a etapa seguinte de modelagem, focada na segmentação de clientes.

---



### 4.3. Segmentação de Clientes (RFM e K-Means)

A principal solução analítica desenvolvida neste projeto foi a segmentação de clientes, utilizando duas abordagens: análise RFM baseada em scores e clustering K-Means. O script `customer_segmentation_corrected.py` implementa ambas as técnicas.

**1. Cálculo RFM:**

*   **Recência (R):** Calculada como o número de dias entre a última compra do cliente e uma data de referência (o dia seguinte à última data no dataset).
*   **Frequência (F):** Calculada como o número total de pedidos únicos realizados pelo cliente.
*   **Valor Monetário (M):** Calculado como a soma total gasta pelo cliente em todos os seus pedidos.

```python
# Trecho de customer_segmentation_corrected.py - Cálculo RFM

max_date = df["Date"].max()
reference_date = max_date + dt.timedelta(days=1)

rfm_df = df.groupby("CustomerID").agg(
    Recency=("Date", lambda date: (reference_date - date.max()).days),
    Frequency=("OrderID", "nunique"),
    MonetaryValue=("TotalPrice", "sum")
).reset_index()
```

**2. Scoring RFM:**

*   Scores de 1 a 5 foram atribuídos para cada métrica (R, F, M) usando quantis (`pd.qcut`). Para Recência, um score maior indica menor recência (melhor). Para Frequência e Valor Monetário, um score maior indica maior frequência/valor (melhor).
*   Um score RFM combinado (ex: '543') e um score de soma (R+F+M) foram criados.

```python
# Trecho de customer_segmentation_corrected.py - Scoring RFM

r_labels = range(5, 0, -1)
f_labels = range(1, 6)
m_labels = range(1, 6)

rfm_df["R_Score"] = pd.qcut(rfm_df["Recency"], q=5, labels=r_labels, duplicates="drop").astype(int)
rfm_df["F_Score"] = pd.qcut(rfm_df["Frequency"].rank(method="first"), q=5, labels=f_labels, duplicates="drop").astype(int)
rfm_df["M_Score"] = pd.qcut(rfm_df["MonetaryValue"], q=5, labels=m_labels, duplicates="drop").astype(int)
```

**3. Segmentação Baseada em Scores RFM:**

*   Segmentos pré-definidos (como 'Campeões', 'Clientes Leais', 'Hibernando', etc.) foram atribuídos com base em regras aplicadas aos scores R e F.
*   A distribuição dos clientes por esses segmentos foi visualizada (ver `09_rfm_segment_distribution.png`).

**4. Segmentação com K-Means (Opcional):**

*   Como alternativa, aplicou-se o algoritmo K-Means sobre as métricas RFM.
*   Os dados RFM foram transformados (logaritmo) e padronizados (StandardScaler) para adequar ao algoritmo.
*   O método do cotovelo (Elbow Method) foi usado para sugerir um número ótimo de clusters (k=4 neste caso, ver `10_kmeans_elbow_method.png`).
*   O K-Means foi executado com k=4, e os clusters resultantes foram analisados e visualizados (ver `11_kmeans_clusters_2d.png`).

```python
# Trecho de customer_segmentation_corrected.py - K-Means

rfm_log = np.log1p(rfm_for_clustering)
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_log)

# ... (código do método do cotovelo)

k_optimal = 4
kmeans = KMeans(n_clusters=k_optimal, init="k-means++", n_init=10, random_state=42)
rfm_df["KMeans_Cluster"] = kmeans.fit_predict(rfm_scaled_df)
```

Os resultados da segmentação (incluindo scores RFM, segmento RFM e cluster K-Means) foram salvos no arquivo `customer_segments.csv`.

---

## 5. Resultados e Discussão

A análise exploratória revelou padrões importantes, como a concentração de vendas em determinadas categorias e a variação ao longo do tempo e dias da semana. A segmentação de clientes forneceu uma visão clara dos diferentes grupos de consumidores:

*   **Segmentos RFM:** A análise baseada em scores permitiu identificar grupos como 'Campeões' (alta frequência e valor, baixa recência) e 'Hibernando' (baixa frequência e valor, alta recência), direcionando estratégias de marketing específicas para cada um.
*   **Clusters K-Means:** A abordagem K-Means agrupou clientes com base na similaridade de seus perfis RFM, oferecendo uma segmentação alternativa baseada em proximidade matemática nos dados transformados.

Ambas as abordagens de segmentação oferecem valor, permitindo à empresa focar esforços de retenção, reativação e aquisição de forma mais eficiente.

## 6. Conclusão e Próximos Passos

Este projeto demonstrou com sucesso a aplicação de técnicas de ciência de dados, utilizando Python e SQL, para analisar dados de vendas no varejo e segmentar clientes. Os resultados fornecem insights valiosos para a tomada de decisão estratégica.

**Próximos Passos Possíveis:**

*   **Aprofundar Análises:** Investigar a cesta de compras (market basket analysis) para identificar produtos frequentemente comprados juntos.
*   **Modelagem Preditiva:** Desenvolver modelos para prever o churn de clientes ou o lifetime value (LTV).
*   **Dashboard Interativo:** Criar um dashboard (ex: usando Streamlit, Dash ou Power BI) para visualização interativa dos resultados.
*   **Deploy:** Implementar a lógica de segmentação em um ambiente de produção para atualização periódica.

## 7. Estrutura do Projeto e Arquivos

*   `/home/ubuntu/`
    *   `generate_data.py`: Script Python para gerar o dataset sintético.
    *   `eda_analysis.py`: Script Python para limpeza, pré-processamento e análise exploratória.
    *   `customer_segmentation_corrected.py`: Script Python para cálculo RFM e segmentação (Scores e K-Means).
    *   `online_sales_raw.csv`: Dataset bruto gerado.
    *   `online_sales_processed.csv`: Dataset limpo e pré-processado.
    *   `customer_segments.csv`: Dataset final com os segmentos de clientes.
    *   `sales_database.db`: Banco de dados SQLite contendo a tabela `sales_processed`.
    *   `projeto_ciencia_dados_varejo.md`: Este relatório.
    *   `01_problem_statement.md`: Arquivo inicial com a definição do problema (incorporado neste relatório).
    *   `02_data_plan.md`: Arquivo inicial com o plano de dados (incorporado neste relatório).
    *   `todo.md`: Checklist de acompanhamento das tarefas.
    *   `plots/`: Diretório contendo todos os gráficos gerados:
        *   `01_numeric_distributions.png`
        *   `02_monthly_sales_trend.png`
        *   `03_sales_by_category.png`
        *   `04_sales_by_region.png`
        *   `05_top_10_products.png`
        *   `06_sales_by_dayofweek.png`
        *   `07_sales_by_hour.png`
        *   `08_payment_method_distribution.png`
        *   `09_rfm_segment_distribution.png`
        *   `10_kmeans_elbow_method.png`
        *   `11_kmeans_clusters_2d.png`

---

