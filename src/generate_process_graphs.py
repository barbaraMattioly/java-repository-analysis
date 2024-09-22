import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Função para criar gráficos das métricas de processo
def plot_process_metrics(data_file):
    # Carrega os dados do CSV
    df = pd.read_csv(data_file)

    # Converte valores de métricas de processo para o tipo float (se necessário)
    process_metrics = ['Total de Estrelas', 'Total de Releases', 'Idade do Repositório (anos)']
    for metric in process_metrics:
        df[metric] = pd.to_numeric(df[metric], errors='coerce')

    # Cria gráficos para cada métrica de processo
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    sns.histplot(df['Total de Estrelas'], bins=20, kde=True, ax=axes[0])
    axes[0].set_title('Distribuição de Estrelas (Popularidade)')
    axes[0].set_xlabel('Número de Estrelas')
    axes[0].set_ylabel('Quantidade')

    sns.histplot(df['Total de Releases'], bins=20, kde=True, ax=axes[1])
    axes[1].set_title('Distribuição de Releases (Atividade)')
    axes[1].set_xlabel('Número de Releases')
    axes[1].set_ylabel('Quantidade')

    sns.histplot(df['Idade do Repositório (anos)'], bins=20, kde=True, ax=axes[2])
    axes[2].set_title('Distribuição da Idade (Maturidade)')
    axes[2].set_xlabel('Idade do Repositório (anos)')
    axes[2].set_ylabel('Quantidade')

    plt.tight_layout()
    plt.show()

# Main
if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, "repos_info.csv")
    plot_process_metrics(file_path)
