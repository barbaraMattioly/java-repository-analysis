import os
import subprocess
import time
import shutil
import csv
import concurrent.futures

# Função para clonar o repositório
def clone_repo(repo_url, repo_name):
    if not os.path.exists(repo_name):
        print(f"Clonando repositório {repo_name}...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, repo_name], check=True)

# Função para executar o CK no repositório clonado
def run_ck_on_repo(repo_name):
    ck_jar_path = "C:/Program Files/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"  # Caminho para o jar do CK
    output_dir = os.path.join("ck_results", repo_name)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Executando CK no repositório {repo_name}...")

    # Executa o CK no repositório clonado
    subprocess.run(["java", "-jar", ck_jar_path, repo_name], check=True)
    
    # Move os arquivos CSV gerados para a pasta ck_results/repo_name
    for file in os.listdir("."):  # Verifica os arquivos na raiz do diretório atual
        if file.endswith(".csv"):
            shutil.move(file, os.path.join(output_dir, file))

# Função para remover o repositório clonado
def remove_cloned_repo(repo_name):
    print(f"Removendo repositório {repo_name}...")
    folder_path = os.path.join(os.getcwd(), repo_name)
    
    # Verifica se o diretório existe antes de tentar removê-lo
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path, ignore_errors=True)
        print(f"Repositório {repo_name} removido com sucesso.")
    else:
        print(f"Diretório {folder_path} não encontrado.")

# Função para processar um único repositório (para ser usado em paralelo)
def process_repo(repo):
    repo_url = repo["url"]
    repo_name = repo["name"]

    try:
        # 1. Clonar o repositório
        clone_repo(repo_url, repo_name)
        
        # 2. Executar o CK no repositório clonado
        run_ck_on_repo(repo_name)
        
        # 3. Remover o repositório clonado da máquina para economizar espaço
        remove_cloned_repo(repo_name)
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao processar o repositório {repo_name}: {e}")

# Função para processar múltiplos repositórios em paralelo
def process_multiple_repos_parallel(repo_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submete as tarefas para serem executadas em paralelo
        futures = [executor.submit(process_repo, repo) for repo in repo_list]
        
        # Aguarda todas as tarefas terminarem
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Verifica exceções
            except Exception as e:
                print(f"Erro durante o processamento: {e}")

# Le a lista de repositórios armazenados após extração da API do GitHub
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
    
    # Processa todos os repositórios da lista em paralelo
    start_time = time.time()
    process_multiple_repos_parallel(repo_list)
    end_time = time.time()

    print(f"Processamento completo em {end_time - start_time:.2f} segundos.")