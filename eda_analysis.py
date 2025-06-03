import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os

# --- Configurações e Funções Auxiliares ---

# Diretório para salvar gráficos
output_plot_dir = '/home/ubuntu/plots'
if not os.path.exists(output_plot_dir):
    os.makedirs(output_plot_dir)

# Configurações de plotagem
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["axes.titlesize"] = 16
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10

def save_plot(filename, fig=None):
    """Salva a figura atual ou especificada no diretório de plots."""
    if fig:
        fig.savefig(os.path.join(output_plot_dir, filename), bbox_inches='tight')
    else:
        plt.savefig(os.path.join(output_plot_dir, filename), bbox_inches='tight')
    plt.close() # Fecha a figura para liberar memória
    print(f"Gráfico salvo: {filename}")

# --- Carregamento e Limpeza Inicial (Conforme Plano) ---

raw_data_path = '/home/ubuntu/online_sales_raw.csv'
processed_data_path = '/home/ubuntu/online_sales_processed.csv'
db_path = '/home/ubuntu/sales_database.db'

print(f"Carregando dados de {raw_data_path}...")
df = pd.read_csv(raw_data_path, parse_dates=["Date"])

print("\nInformações iniciais do DataFrame:")
df.info()

print("\nVerificando valores nulos iniciais:")
print(df.isnull().sum())

# Tratamento de Nulos (Exemplo: preencher CustomerID com -1 ou remover; remover linhas com Region nula)
initial_rows = len(df)
df['CustomerID'] = df['CustomerID'].fillna(-1).astype(int) # Preenche com -1 e converte para int
df.dropna(subset=['Region'], inplace=True) # Remove linhas com Região nula

print(f"\nLinhas removidas por NaN em 'Region': {initial_rows - len(df)}")
print("Valores nulos após tratamento inicial:")
print(df.isnull().sum())

# Verificação de Duplicatas
duplicates = df.duplicated().sum()
if duplicates > 0:
    print(f"\nRemovendo {duplicates} linhas duplicadas...")
    df.drop_duplicates(inplace=True)
else:
    print("\nNenhuma linha duplicada encontrada.")

# Conversão de Tipos (já feito parcialmente no read_csv e tratamento de nulos)
# Garantir que outras colunas estejam corretas se necessário

# --- Engenharia de Atributos ---
print("\nCriando atributos de data...")
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Week'] = df['Date'].dt.isocalendar().week.astype(int)
df['DayOfWeek'] = df['Date'].dt.dayofweek # Segunda=0, Domingo=6
df['Hour'] = df['Date'].dt.hour
df['DateOnly'] = df['Date'].dt.date

print("Novas colunas criadas:", ['Year', 'Month', 'Week', 'DayOfWeek', 'Hour', 'DateOnly'])

# --- Análise Exploratória de Dados (EDA) ---

print("\n--- Iniciando Análise Exploratória de Dados (EDA) ---")

# 1. Estatísticas Descritivas
print("\nEstatísticas Descritivas das colunas numéricas:")
print(df[['Quantity', 'UnitPrice', 'TotalPrice']].describe())

# 2. Distribuição das Variáveis Numéricas
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.histplot(df['Quantity'], bins=30, kde=True, ax=axes[0]).set_title('Distribuição da Quantidade')
sns.histplot(df['UnitPrice'], bins=30, kde=True, ax=axes[1]).set_title('Distribuição do Preço Unitário')
sns.histplot(df['TotalPrice'], bins=30, kde=True, ax=axes[2]).set_title('Distribuição do Preço Total')
plt.tight_layout()
save_plot('01_numeric_distributions.png', fig)

# 3. Vendas ao Longo do Tempo
print("\nAnalisando vendas ao longo do tempo...")
# Agrupar por Mês
df_monthly_sales = df.set_index('Date').resample('M')['TotalPrice'].sum().reset_index()
fig = plt.figure()
plt.plot(df_monthly_sales['Date'], df_monthly_sales['TotalPrice'], marker='o')
plt.title('Vendas Totais Mensais')
plt.xlabel('Mês')
plt.ylabel('Vendas Totais')
plt.xticks(rotation=45)
plt.tight_layout()
save_plot('02_monthly_sales_trend.png', fig)

# 4. Vendas por Categoria
print("\nAnalisando vendas por categoria...")
category_sales = df.groupby('Category')['TotalPrice'].sum().sort_values(ascending=False)
fig = plt.figure()
sns.barplot(x=category_sales.values, y=category_sales.index, palette='viridis')
plt.title('Vendas Totais por Categoria')
plt.xlabel('Vendas Totais')
plt.ylabel('Categoria')
plt.tight_layout()
save_plot('03_sales_by_category.png', fig)

# 5. Vendas por Região
print("\nAnalisando vendas por região...")
region_sales = df.groupby('Region')['TotalPrice'].sum().sort_values(ascending=False)
fig = plt.figure()
sns.barplot(x=region_sales.values, y=region_sales.index, palette='magma')
plt.title('Vendas Totais por Região')
plt.xlabel('Vendas Totais')
plt.ylabel('Região')
plt.tight_layout()
save_plot('04_sales_by_region.png', fig)

# 6. Top Produtos Mais Vendidos (por Quantidade e Receita)
print("\nAnalisando top produtos...")
top_products_quantity = df.groupby('ProductName')['Quantity'].sum().nlargest(10)
top_products_revenue = df.groupby('ProductName')['TotalPrice'].sum().nlargest(10)

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
sns.barplot(x=top_products_quantity.values, y=top_products_quantity.index, ax=axes[0], palette='coolwarm').set_title('Top 10 Produtos por Quantidade Vendida')
sns.barplot(x=top_products_revenue.values, y=top_products_revenue.index, ax=axes[1], palette='Spectral').set_title('Top 10 Produtos por Receita Gerada')
plt.tight_layout()
save_plot('05_top_10_products.png', fig)

# 7. Vendas por Dia da Semana
print("\nAnalisando vendas por dia da semana...")
day_names = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
dayofweek_sales = df.groupby('DayOfWeek')['TotalPrice'].sum()
dayofweek_sales.index = dayofweek_sales.index.map(lambda x: day_names[x])
dayofweek_sales = dayofweek_sales.reindex(day_names)

fig = plt.figure()
sns.barplot(x=dayofweek_sales.index, y=dayofweek_sales.values, palette='cubehelix')
plt.title('Vendas Totais por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Vendas Totais')
plt.tight_layout()
save_plot('06_sales_by_dayofweek.png', fig)

# 8. Vendas por Hora do Dia
print("\nAnalisando vendas por hora do dia...")
hourly_sales = df.groupby('Hour')['TotalPrice'].sum()
fig = plt.figure()
sns.lineplot(x=hourly_sales.index, y=hourly_sales.values, marker='o')
plt.title('Vendas Totais por Hora do Dia')
plt.xlabel('Hora do Dia')
plt.ylabel('Vendas Totais')
plt.xticks(range(0, 24))
plt.grid(True)
plt.tight_layout()
save_plot('07_sales_by_hour.png', fig)

# 9. Uso de Métodos de Pagamento
print("\nAnalisando métodos de pagamento...")
payment_usage = df['PaymentMethod'].value_counts()
fig = plt.figure()
payment_usage.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap='tab20c')
plt.title('Distribuição de Métodos de Pagamento')
plt.ylabel('') # Remover label do eixo y para pie chart
plt.tight_layout()
save_plot('08_payment_method_distribution.png', fig)

# --- Salvar Dados Processados e Carregar no SQLite (Opcional) ---

print(f"\nSalvando dados processados em {processed_data_path}...")
df.to_csv(processed_data_path, index=False, date_format='%Y-%m-%d %H:%M:%S')

# Opcional: Carregar no SQLite
try:
    print(f"Conectando ao banco de dados SQLite: {db_path}")
    conn = sqlite3.connect(db_path)
    print("Carregando dados processados para a tabela 'sales_processed'...")
    # Usar 'replace' para substituir a tabela se ela já existir
    df.to_sql('sales_processed', conn, if_exists='replace', index=False)
    print("Dados carregados com sucesso no SQLite.")

    # Exemplo de consulta SQL pós-carga
    print("\nExemplo de consulta SQL (Top 5 Categorias por Venda Total):")
    query = "SELECT Category, SUM(TotalPrice) as TotalSales FROM sales_processed GROUP BY Category ORDER BY TotalSales DESC LIMIT 5;"
    top_categories_sql = pd.read_sql_query(query, conn)
    print(top_categories_sql)

    conn.close()
    print("Conexão com SQLite fechada.")
except Exception as e:
    print(f"Erro ao interagir com o SQLite: {e}")

print("\n--- Análise Exploratória de Dados Concluída ---")

