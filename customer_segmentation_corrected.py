import pandas as pd
import numpy as np
import sqlite3
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

# --- Configurações e Funções Auxiliares ---

db_path = '/home/ubuntu/sales_database.db'
processed_data_path = '/home/ubuntu/online_sales_processed.csv'
output_plot_dir = '/home/ubuntu/plots'
output_segmented_data_path = '/home/ubuntu/customer_segments.csv'

# Garante que o diretório de plots exista
if not os.path.exists(output_plot_dir):
    os.makedirs(output_plot_dir)

# Configurações de plotagem
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

def save_plot(filename, fig=None):
    """Salva a figura atual ou especificada no diretório de plots."""
    if fig:
        fig.savefig(os.path.join(output_plot_dir, filename), bbox_inches='tight')
    else:
        plt.savefig(os.path.join(output_plot_dir, filename), bbox_inches='tight')
    plt.close() # Fecha a figura para liberar memória
    print(f"Gráfico salvo: {filename}")

# --- Carregamento dos Dados Processados ---

print(f"Carregando dados processados de {processed_data_path}...")
# Ler CustomerID como string inicialmente para evitar problemas com -1 se lido como float
df = pd.read_csv(processed_data_path, parse_dates=["Date"], dtype={'CustomerID': str})

# Filtrar clientes válidos (excluir o ID -1 usado para preencher NaNs, se houver)
df = df[df["CustomerID"] != '-1']
df["CustomerID"] = df["CustomerID"].astype(int) # Converter para int após filtrar

print(f"Número de registros após filtrar clientes inválidos: {len(df)}")

# --- Cálculo RFM (Recency, Frequency, Monetary) ---

print("\n--- Iniciando Cálculo RFM ---")

# Definir a data de referência para cálculo da Recência (um dia após a última data no dataset)
max_date = df["Date"].max()
reference_date = max_date + dt.timedelta(days=1)
print(f"Data de referência para Recência: {reference_date.strftime('%Y-%m-%d')}")

# Calcular RFM usando agregação com Pandas
rfm_df = df.groupby("CustomerID").agg(
    Recency=("Date", lambda date: (reference_date - date.max()).days),
    Frequency=("OrderID", "nunique"),
    MonetaryValue=("TotalPrice", "sum")
).reset_index()

print("\nDataFrame RFM inicial:")
print(rfm_df.head())
print(f"\nNúmero de clientes únicos: {len(rfm_df)}")

# --- Scoring RFM --- 

print("\n--- Calculando Scores RFM (usando quantis) ---")

# Criar labels para os scores (1=pior, 5=melhor)
r_labels = range(5, 0, -1)
f_labels = range(1, 6)
m_labels = range(1, 6)

# Calcular scores usando qcut
rfm_df["R_Score"] = pd.qcut(rfm_df["Recency"], q=5, labels=r_labels, duplicates='drop').astype(int)
rfm_df["F_Score"] = pd.qcut(rfm_df["Frequency"].rank(method='first'), q=5, labels=f_labels, duplicates='drop').astype(int)
rfm_df["M_Score"] = pd.qcut(rfm_df["MonetaryValue"], q=5, labels=m_labels, duplicates='drop').astype(int)

print("\nScores RFM calculados:")
print(rfm_df[["CustomerID", "Recency", "Frequency", "MonetaryValue", "R_Score", "F_Score", "M_Score"]].head())

# Combinar scores para obter RFM_Score
rfm_df["RFM_Score"] = rfm_df["R_Score"].astype(str) + rfm_df["F_Score"].astype(str) + rfm_df["M_Score"].astype(str)

# Calcular score agregado
rfm_df["RFM_Sum_Score"] = rfm_df["R_Score"] + rfm_df["F_Score"] + rfm_df["M_Score"]

# --- Segmentação Baseada em Scores RFM ---

print("\n--- Segmentando clientes com base nos Scores RFM ---")

segment_map = {
    r'[1-2][1-2]': 'Hibernando',
    r'[1-2][3-4]': 'Em Risco',
    r'[1-2]5': 'Não Pode Perder',
    r'3[1-2]': 'Quase Dormindo',
    r'33': 'Precisa Atenção',
    r'[3-4][4-5]': 'Clientes Leais',
    r'41': 'Promissor',
    r'51': 'Novos Clientes',
    r'[4-5][2-3]': 'Potenciais Leais',
    r'5[4-5]': 'Campeões'
}

rfm_df["Segment_RFM_Score"] = rfm_df["R_Score"].astype(str) + rfm_df["F_Score"].astype(str)
rfm_df["Segment"] = rfm_df["Segment_RFM_Score"].replace(segment_map, regex=True)

print("\nDistribuição dos Segmentos RFM:")
segment_counts = rfm_df["Segment"].value_counts()
print(segment_counts)

# Visualizar distribuição dos segmentos
fig = plt.figure(figsize=(12, 7))
sns.barplot(x=segment_counts.values, y=segment_counts.index, palette='viridis')
plt.title("Distribuição dos Clientes por Segmento RFM")
plt.xlabel("Número de Clientes")
plt.ylabel("Segmento")
save_plot("09_rfm_segment_distribution.png", fig)

# --- Análise dos Segmentos --- 

print("\n--- Análise Média RFM por Segmento ---")
segment_analysis = rfm_df.groupby("Segment").agg(
    Recency_Media=("Recency", "mean"),
    Frequencia_Media=("Frequency", "mean"),
    Valor_Monetario_Medio=("MonetaryValue", "mean"),
    Contagem_Clientes=("MonetaryValue", "count")
).round(1)

print(segment_analysis)

# --- (Opcional) Segmentação com K-Means --- 

print("\n--- Iniciando Segmentação com K-Means (Opcional) ---")

# Selecionar apenas as métricas RFM para clustering
rfm_for_clustering = rfm_df[["Recency", "Frequency", "MonetaryValue"]]

# Lidar com valores extremos (ex: usando log transform)
rfm_log = np.log1p(rfm_for_clustering)

# Padronizar os dados
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_log)
rfm_scaled_df = pd.DataFrame(rfm_scaled, index=rfm_df.index, columns=['Recency', 'Frequency', 'MonetaryValue'])

# Determinar número ótimo de clusters (Método do Cotovelo)
print("Calculando WCSS para o Método do Cotovelo...")
wcss = {}
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300, random_state=42)
    kmeans.fit(rfm_scaled_df)
    wcss[k] = kmeans.inertia_

# Plotar o gráfico do cotovelo
fig = plt.figure()
plt.plot(list(wcss.keys()), list(wcss.values()), marker='o')
plt.title("Método do Cotovelo para K-Means")
plt.xlabel("Número de Clusters (k)")
plt.ylabel("WCSS (Within-Cluster Sum of Squares)")
plt.grid(True)
save_plot("10_kmeans_elbow_method.png", fig)

# Escolher o número de clusters (ex: baseado no cotovelo, digamos k=4)
k_optimal = 4
print(f"\nExecutando K-Means com k={k_optimal}...")
kmeans = KMeans(n_clusters=k_optimal, init='k-means++', n_init=10, max_iter=300, random_state=42)
rfm_df["KMeans_Cluster"] = kmeans.fit_predict(rfm_scaled_df)

print("\nDistribuição dos Clusters K-Means:")
cluster_counts = rfm_df["KMeans_Cluster"].value_counts()
print(cluster_counts)

# Analisar características dos clusters K-Means
print("\n--- Análise Média RFM por Cluster K-Means ---")
kmeans_analysis = rfm_df.groupby("KMeans_Cluster").agg(
    Recency_Media=("Recency", "mean"),
    Frequencia_Media=("Frequency", "mean"),
    Valor_Monetario_Medio=("MonetaryValue", "mean"),
    Contagem_Clientes=("MonetaryValue", "count")
).round(1)

print(kmeans_analysis)

# Visualizar Clusters (exemplo 2D - Recency vs Monetary)
fig = plt.figure(figsize=(10, 8))
sns.scatterplot(data=rfm_df, x='Recency', y='MonetaryValue', hue='KMeans_Cluster', palette='Set1', s=50, alpha=0.7)
plt.title("Clusters K-Means (Recency vs MonetaryValue)")
plt.xlabel("Recência (Dias)")
plt.ylabel("Valor Monetário Total")
plt.legend(title='Cluster')
save_plot("11_kmeans_clusters_2d.png", fig)

# --- Salvar Resultados da Segmentação ---

# Remover coluna auxiliar antes de salvar
rfm_df_final = rfm_df.drop(columns=['Segment_RFM_Score'])

print(f"\nSalvando dados segmentados em {output_segmented_data_path}...")
rfm_df_final.to_csv(output_segmented_data_path, index=False)

print("\n--- Análise de Segmentação Concluída ---")

