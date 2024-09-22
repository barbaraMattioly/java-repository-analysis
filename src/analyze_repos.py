import pandas as pd
import os
import csv

# Função para sumarizar as métricas de todos os repositórios e salvar em CSV
def summarize_all_repos(repo_list, csv_file="ck_summary.csv"):
    all_summary_data = []
    
    for repo in repo_list:
        repo_name = repo["name"]
        output_dir = os.path.join("ck_results", repo_name)

        ck_files = [file for file in os.listdir(output_dir) if file.endswith(".csv")]
        
        summary_data = {"repo_name": repo_name}

        for ck_file in ck_files:
            file_path = os.path.join(output_dir, ck_file)
            
            # Lê o CSV gerado pelo CK
            df = pd.read_csv(file_path)

            # Métricas que serão sumarizadas
            metrics = ["cbo", "dit", "lcom", "loc"]

            for metric in metrics:
                if metric in df.columns:
                    summary_data[f"{metric}_mean"] = round(df[metric].mean(), 3)
                    summary_data[f"{metric}_median"] = round(df[metric].median(), 3)
                    summary_data[f"{metric}_std_dev"] = round(df[metric].std(), 3)
        
        all_summary_data.append(summary_data)

    summary_df = pd.DataFrame(all_summary_data)
    summary_df.to_csv(csv_file, index=False)


# Le a lista de repositórios armazenados após extração da api do github
def read_repos_from_csv(file_path):
    repo_list = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            repo_list.append({
                "url": row["URL"],
                "name": row["Nome do Repositório"]
            })
    return repo_list

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'repos_info.csv')
    repo_list = read_repos_from_csv(file_path)
    
    # Processa todos os repositórios da lista
    summarize_all_repos(repo_list)