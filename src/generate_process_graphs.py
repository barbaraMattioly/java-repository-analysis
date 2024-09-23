import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Função para criar gráficos das métricas de processo e LOC
def plot_metrics_with_loc(process_file, ck_file):
    # Carrega os dados do CSV de métricas de processo
    df_process = pd.read_csv(process_file)
    
    # Carrega o arquivo de métricas CK, incluindo o LOC
    df_ck = pd.read_csv(ck_file)

    # Converte valores de métricas de processo para o tipo float (se necessário)
    process_metrics = ['Total de Estrelas', 'Total de Releases', 'Idade do Repositório (anos)']
    for metric in process_metrics:
        df_process[metric] = pd.to_numeric(df_process[metric], errors='coerce')

    # Converte o LOC do arquivo CK para float, se necessário
    df_ck['loc_mean'] = pd.to_numeric(df_ck['loc_mean'], errors='coerce')

    # Cria gráficos para cada métrica de processo
    fig, axes = plt.subplots(2, 2, figsize=(18, 10))  # Layout 2x2 para incluir LOC

    sns.histplot(df_process['Total de Estrelas'], bins=20, kde=True, ax=axes[0, 0])
    axes[0, 0].set_title('Distribuição de Estrelas (Popularidade)')
    axes[0, 0].set_xlabel('Número de Estrelas')
    axes[0, 0].set_ylabel('Quantidade')

    sns.histplot(df_process['Total de Releases'], bins=20, kde=True, ax=axes[0, 1])
    axes[0, 1].set_title('Distribuição de Releases (Atividade)')
    axes[0, 1].set_xlabel('Número de Releases')
    axes[0, 1].set_ylabel('Quantidade')

    sns.histplot(df_process['Idade do Repositório (anos)'], bins=20, kde=True, ax=axes[1, 0])
    axes[1, 0].set_title('Distribuição da Idade (Maturidade)')
    axes[1, 0].set_xlabel('Idade do Repositório (anos)')
    axes[1, 0].set_ylabel('Quantidade')

    sns.histplot(df_ck['loc_mean'], bins=20, kde=True, ax=axes[1, 1])
    axes[1, 1].set_title('Distribuição do LOC (Tamanho do Código)')
    axes[1, 1].set_xlabel('LOC (Lines of Code)')
    axes[1, 1].set_ylabel('Quantidade')
    plt.tight_layout()
    plt.show()

# Main
if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    process_file_path = os.path.join(directory, "repos_info.csv")  # Arquivo de métricas de processo
    ck_file_path = os.path.join(directory, "ck_summary.csv")  # Arquivo de métricas CK que contém o LOC
    plot_metrics_with_loc(process_file_path, ck_file_path)
