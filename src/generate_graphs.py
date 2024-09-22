import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

# Carrega os dados do arquivo CSV com as métricas sumarizadas
df = pd.read_csv('c:/Users/dtiDigital/Documents/puc/java-repository-analysis/src/ck_summary.csv')

# Remove linhas com dados faltantes, se necessário
df_clean = df.dropna()

# Lista de métricas para analisar a correlação
metrics = ["cbo_mean", "dit_mean", "lcom_mean"]

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
            plt.title(f'Correlação entre {metric_x} e {metric_y}')
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
