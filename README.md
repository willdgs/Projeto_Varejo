# Projeto de Ciência de Dados: Análise de Vendas e Segmentação de Clientes no Varejo

## Visão Geral

Este repositório contém um projeto completo de ciência de dados focado na análise de dados de vendas de uma empresa de varejo fictícia. O objetivo principal é demonstrar um fluxo de trabalho de ponta a ponta, desde a geração e tratamento de dados até a análise exploratória (EDA) e a segmentação de clientes utilizando Python e SQL.

O projeto foi desenvolvido como um exemplo prático para portfólio, mostrando habilidades em manipulação de dados, visualização, modelagem (clustering) e documentação técnica.

## Tecnologias Utilizadas

*   **Linguagem Principal:** Python 3.11
*   **Bibliotecas Python:**
    *   Pandas: Manipulação e análise de dados.
    *   NumPy: Operações numéricas.
    *   Matplotlib & Seaborn: Visualização de dados.
    *   Scikit-learn: Segmentação com K-Means e pré-processamento.
*   **Banco de Dados:** SQLite (para demonstrar integração SQL).
*   **Formato de Documentação:** Markdown.

## Estrutura do Projeto

```
/
|-- generate_data.py             # Script para gerar dados sintéticos
|-- eda_analysis.py              # Script para limpeza, EDA e carga no SQLite
|-- customer_segmentation_corrected.py # Script para cálculo RFM e segmentação
|-- online_sales_raw.csv         # Dados brutos gerados
|-- online_sales_processed.csv   # Dados limpos e processados
|-- customer_segments.csv        # Dados finais com segmentos de clientes
|-- sales_database.db            # Banco de dados SQLite com dados processados
|-- projeto_ciencia_dados_varejo.md # Relatório detalhado do projeto
|-- plots/                         # Diretório com os gráficos gerados
|   |-- 01_numeric_distributions.png
|   |-- 02_monthly_sales_trend.png
|   |-- ... (outros gráficos)
|-- README.md                    # Este arquivo
|-- todo.md                      # Checklist de acompanhamento (interno)
|-- .gitignore                   # Arquivo para ignorar arquivos no Git (será criado)
```

## Como Executar

1.  **Clone o Repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_DIRETORIO>
    ```
2.  **Crie um Ambiente Virtual (Recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate  # Windows
    ```
3.  **Instale as Dependências:**
    ```bash
    pip install pandas numpy matplotlib seaborn scikit-learn
    ```
    *(Nota: O SQLite geralmente já vem com o Python)*

4.  **Execute os Scripts na Ordem:**
    *   Gere os dados brutos:
        ```bash
        python generate_data.py
        ```
    *   Execute a limpeza, EDA e carregue no SQLite:
        ```bash
        python eda_analysis.py
        ```
    *   Execute a segmentação de clientes:
        ```bash
        python customer_segmentation_corrected.py
        ```

5.  **Explore os Resultados:**
    *   Verifique os arquivos CSV gerados (`online_sales_processed.csv`, `customer_segments.csv`).
    *   Analise os gráficos na pasta `plots/`.
    *   Consulte o banco de dados `sales_database.db` usando uma ferramenta de sua preferência (ex: DB Browser for SQLite) ou via Python.
    *   Leia o relatório `projeto_ciencia_dados_varejo.md` para um entendimento completo do processo e dos insights.

## Principais Etapas e Resultados

1.  **Geração de Dados:** Criação de um dataset sintético realista com 50.000 transações.
2.  **Limpeza e Pré-processamento:** Tratamento de valores nulos, verificação de duplicatas, conversão de tipos e engenharia de atributos (extração de componentes de data).
3.  **Análise Exploratória (EDA):** Visualização de tendências de vendas, desempenho por categoria/região, identificação de top produtos e análise de padrões temporais.
4.  **Segmentação de Clientes:**
    *   **RFM (Recência, Frequência, Valor Monetário):** Cálculo das métricas RFM, atribuição de scores e criação de segmentos baseados em regras (ex: Campeões, Hibernando).
    *   **K-Means:** Aplicação do algoritmo K-Means sobre os dados RFM transformados para obter uma segmentação alternativa baseada em clusters.
5.  **Documentação:** Relatório detalhado explicando cada fase do projeto, as decisões tomadas e os resultados obtidos.

## Autor

*   Willian

*(Este projeto foi originalmente desenvolvido com o auxílio da IA Manus)*

