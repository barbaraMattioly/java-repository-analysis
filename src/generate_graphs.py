import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

# Carrega os dados do arquivo CSV com as métricas sumarizadas
directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(directory, "ck_summary.csv")

# Carrega o arquivo CSV em um DataFrame
df = pd.read_csv(file_path)

# Remove linhas com dados faltantes, se necessário
df_clean = df.dropna()

# Nomes completos das métricas
metric_names = {
    "cbo_mean": "Coupling between Objects (CBO)",
    "dit_mean": "Depth of Inheritance Tree (DIT)",
    "lcom_mean": "Lack of Cohesion of Methods (LCOM)",
    "loc_mean": "Lines of Code (LOC)"
}

# Lista de métricas para analisar a correlação
metrics = ["cbo_mean", "dit_mean", "lcom_mean", "loc_mean"]

# Função para calcular e plotar correlação entre métricas
def plot_correlations(df, metrics):
    # Loop para cada combinação de métricas
    for i in range(len(metrics)):
        for j in range(i+1, len(metrics)):
            metric_x = metrics[i]
            metric_y = metrics[j]
            
            # Criação do gráfico de dispersão com linha de tendência
            plt.figure(figsize=(8, 6))
            sns.regplot(x=df[metric_x], y=df[metric_y], scatter_kws={'s':50}, line_kws={"color":"red"})
            plt.title(f'{metric_names[metric_x]} X {metric_names[metric_y]}')
            plt.xlabel(metric_x)
            plt.ylabel(metric_y)
            plt.grid(True)
            plt.show()

            # Testes de correlação de Pearson e Spearman
            pearson_corr, _ = pearsonr(df[metric_x], df[metric_y])
            spearman_corr, _ = spearmanr(df[metric_x], df[metric_y])
            
            print(f"Correlação de Pearson entre {metric_x} e {metric_y}: {pearson_corr:.3f}")
            print(f"Correlação de Spearman entre {metric_x} e {metric_y}: {spearman_corr:.3f}")
            print('-' * 50)

# Gera os gráficos e executa os testes de correlação
plot_correlations(df_clean, metrics)
