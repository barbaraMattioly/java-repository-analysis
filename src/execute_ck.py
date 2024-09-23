import os
import subprocess
import time
import shutil
import stat
import csv
import concurrent.futures

# Função para clonar o repositório
def clone_repo(repo_url, repo_name, retries=3, delay=5):
    for attempt in range(retries):
        try:
            if not os.path.exists(repo_name):
                print(f"Clonando repositório {repo_name}...")
                subprocess.run(["git", "clone", "--depth", "1", repo_url, repo_name], check=True)
            return
        except subprocess.CalledProcessError as e:
            if attempt < retries - 1:
                print(f"Falha ao clonar {repo_name}, tentando novamente em {delay} segundos...")
                time.sleep(delay)
            else:
                print(f"Falha ao clonar {repo_name} após {retries} tentativas.")
                raise e

# Função para executar o CK no repositório clonado
def run_ck_on_repo(repo_name):
    ck_jar_path = "C:/Program Files/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"  # Caminho para o jar do CK
    output_dir = os.path.join("ck_results", repo_name)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Executando CK no repositório {repo_name}...")

    try:
        # Aumenta a memória do Java com a flag -Xmx2G e o tempo limite para 600 segundos
        subprocess.run(
            ["java", "-Xmx2G", "-jar", ck_jar_path, "."],
            check=True,
            cwd=repo_name,
            timeout=600
        )
        
        for filename in os.listdir(repo_name):
            if filename.endswith(".csv"):  # Move todos os arquivos CSV gerados pelo CK
                shutil.move(os.path.join(repo_name, filename), os.path.join(output_dir, filename))
    
    except subprocess.CalledProcessError as e:
        print(f"Falha ao executar CK no repositório {repo_name}: {e}")
        raise e
    except subprocess.TimeoutExpired:
        print(f"O CK demorou muito para processar o repositório {repo_name} e foi interrompido.")

# Função para alterar permissões e remover o repositório clonado
def remove_cloned_repo(repo_name):
    print(f"Removendo repositório {repo_name}...")
    folder_path = os.path.join(os.getcwd(), repo_name)

    def on_rm_error(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path, onerror=on_rm_error)
            print(f"Repositório {repo_name} removido com sucesso.")
        else:
            print(f"Diretório {folder_path} não encontrado.")
    except Exception as e:
        print(f"Erro ao remover {repo_name}: {e}")
        raise e

# Função para processar um único repositório (para ser usado em paralelo)
def process_repo(repo):
    repo_url = repo["url"]
    repo_name = repo["name"]

    try:
        # 1. Clonar o repositório
        clone_repo(repo_url, repo_name)
        
        # 2. Executar o CK no repositório clonado
        run_ck_on_repo(repo_name)
        
    except Exception as e:
        print(f"Erro ao processar o repositório {repo_name}: {e}")
    
    finally:
        # 3. Remover o repositório clonado da máquina para economizar espaço
        try:
            remove_cloned_repo(repo_name)
        except Exception as e:
            print(f"Erro ao tentar remover {repo_name}: {e}")

# Função para processar múltiplos repositórios em paralelo
def process_multiple_repos_parallel(repo_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submete as tarefas para serem executadas em paralelo
        futures = [executor.submit(process_repo, repo) for repo in repo_list]
        
        # Aguarda todas as tarefas terminarem
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Erro durante o processamento de um repositório: {e}")

# Lê a lista de repositórios armazenados após extração da API do GitHub
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
