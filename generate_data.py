import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configurações
num_records = 50000
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
num_customers = 1000

categories = ['Eletrônicos', 'Vestuário', 'Casa', 'Livros', 'Esportes', 'Alimentos', 'Beleza']
regions = ['América do Norte', 'Europa', 'Ásia', 'América do Sul', 'Oceania']
payment_methods = ['Cartão de Crédito', 'Boleto', 'PayPal', 'Pix', 'Transferência']

products = {
    'Eletrônicos': ['Smartphone XYZ', 'Laptop ABC', 'Fone de Ouvido QWE', 'Smartwatch 123', 'Tablet ZXC'],
    'Vestuário': ['Camiseta Básica', 'Calça Jeans Slim', 'Jaqueta Corta-Vento', 'Tênis Esportivo', 'Vestido Floral'],
    'Casa': ['Jogo de Panelas', 'Aspirador Robô', 'Luminária de Mesa LED', 'Conjunto de Toalhas', 'Cafeteira Expressa'],
    'Livros': ['Ficção Científica Vol. 1', 'Romance Histórico', 'Biografia Inspiradora', 'Suspense Psicológico', 'Livro de Culinária Vegana'],
    'Esportes': ['Bola de Futebol Oficial', 'Tapete de Yoga', 'Garrafa Térmica', 'Bicicleta Ergométrica', 'Raquete de Tênis Pro'],
    'Alimentos': ['Café Gourmet 500g', 'Azeite Extra Virgem', 'Chocolate Amargo 70%', 'Mix de Castanhas', 'Chá Verde Orgânico'],
    'Beleza': ['Protetor Solar FPS 50', 'Creme Hidratante Facial', 'Shampoo Anticaspa', 'Perfume Floral', 'Kit de Maquiagem Básico']
}

base_prices = {
    'Smartphone XYZ': 2500, 'Laptop ABC': 4500, 'Fone de Ouvido QWE': 300, 'Smartwatch 123': 1200, 'Tablet ZXC': 1800,
    'Camiseta Básica': 50, 'Calça Jeans Slim': 150, 'Jaqueta Corta-Vento': 250, 'Tênis Esportivo': 350, 'Vestido Floral': 200,
    'Jogo de Panelas': 400, 'Aspirador Robô': 1500, 'Luminária de Mesa LED': 120, 'Conjunto de Toalhas': 100, 'Cafeteira Expressa': 600,
    'Ficção Científica Vol. 1': 45, 'Romance Histórico': 55, 'Biografia Inspiradora': 60, 'Suspense Psicológico': 50, 'Livro de Culinária Vegana': 70,
    'Bola de Futebol Oficial': 80, 'Tapete de Yoga': 90, 'Garrafa Térmica': 60, 'Bicicleta Ergométrica': 1300, 'Raquete de Tênis Pro': 450,
    'Café Gourmet 500g': 30, 'Azeite Extra Virgem': 40, 'Chocolate Amargo 70%': 25, 'Mix de Castanhas': 35, 'Chá Verde Orgânico': 20,
    'Protetor Solar FPS 50': 50, 'Creme Hidratante Facial': 80, 'Shampoo Anticaspa': 30, 'Perfume Floral': 180, 'Kit de Maquiagem Básico': 150
}

# Geração dos Dados
data = []
order_id_counter = 1

date_range = (end_date - start_date).days

for i in range(num_records):
    # Cliente Aleatório
    customer_id = random.randint(1001, 1001 + num_customers -1)

    # Data Aleatória
    random_days = random.randint(0, date_range)
    transaction_date = start_date + timedelta(days=random_days, hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))

    # Categoria e Produto Aleatórios
    category = random.choice(categories)
    product_name = random.choice(products[category])

    # Quantidade Aleatória (com viés para quantidades menores)
    quantity = max(1, int(np.random.exponential(scale=1.5)))

    # Preço Unitário (com pequena variação)
    base_price = base_prices[product_name]
    unit_price = round(random.uniform(base_price * 0.95, base_price * 1.05), 2)

    # Preço Total
    total_price = round(quantity * unit_price, 2)

    # Região e Método de Pagamento Aleatórios
    region = random.choice(regions)
    payment_method = random.choice(payment_methods)

    # Adiciona um pouco de dados faltantes (ex: 1% de chance de CustomerID faltante)
    if random.random() < 0.01:
        customer_id_final = np.nan
    else:
        customer_id_final = customer_id

    # Adiciona um pouco de dados faltantes (ex: 0.5% de chance de Região faltante)
    if random.random() < 0.005:
        region_final = np.nan
    else:
        region_final = region

    data.append({
        'OrderID': order_id_counter,
        'CustomerID': customer_id_final,
        'Date': transaction_date,
        'Category': category,
        'ProductName': product_name,
        'Quantity': quantity,
        'UnitPrice': unit_price,
        'TotalPrice': total_price,
        'Region': region_final,
        'PaymentMethod': payment_method
    })
    order_id_counter += 1

# Cria DataFrame
df = pd.DataFrame(data)

# Garante tipo int para CustomerID, permitindo NaNs
df['CustomerID'] = df['CustomerID'].astype('Int64')

# Salva em CSV
output_path = '/home/ubuntu/online_sales_raw.csv'
df.to_csv(output_path, index=False, date_format='%Y-%m-%d %H:%M:%S')

print(f"Dataset sintético gerado e salvo em {output_path}")
print(df.head())
print(f"\nNúmero de registros: {len(df)}")
print(f"Colunas: {df.columns.tolist()}")
print(f"\nTipos de dados:\n{df.dtypes}")

