import os
import subprocess
import time

# Função para clonar o repositório
def clone_repo(repo_url, repo_name):
    if not os.path.exists(repo_name):
        print(f"Clonando repositório {repo_name}...")
        subprocess.run(["git", "clone", repo_url, repo_name], check=True)

# Função para executar o CK no repositório clonado
def run_ck_on_repo(repo_name):
    ck_jar_path = "/path/to/ck.jar"  # Substitua pelo caminho correto
    output_dir = os.path.join("ck_results", repo_name)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Executando CK no repositório {repo_name}...")
    # Executa o CK no repositório clonado
    subprocess.run(["java", "-jar", ck_jar_path, repo_name], check=True)
    
    # Move os arquivos CSV gerados para a pasta de resultados
    for file in os.listdir(repo_name):
        if file.endswith(".csv"):
            os.rename(os.path.join(repo_name, file), os.path.join(output_dir, file))

# Função para remover o repositório clonado
def remove_cloned_repo(repo_name):
    print(f"Removendo repositório {repo_name}...")
    subprocess.run(["rm", "-rf", repo_name], check=True)

# Função para processar múltiplos repositórios
def process_multiple_repos(repo_list):
    for repo in repo_list:
        repo_url = repo["url"]
        repo_name = repo["name"]

        try:
            # 1. Clonar o repositório
            clone_repo(repo_url, repo_name)
            
            # 2. Executar o CK no repositório clonado
            run_ck_on_repo(repo_name)
            
            # 3. (Opcional) Remover o repositório clonado para economizar espaço
            remove_cloned_repo(repo_name)
            
        except subprocess.CalledProcessError as e:
            print(f"Erro ao processar o repositório {repo_name}: {e}")
        
        # Espera um tempo para evitar sobrecarregar o GitHub
        time.sleep(5)

# Exemplo de uso
if __name__ == "__main__":
    # Supondo que você já tenha uma lista dos repositórios
    repo_list = [
        {"url": "https://github.com/elastic/elasticsearch", "name": "repo-java1"},
        {"url": "https://github.com/spring-projects/spring-boot", "name": "repo-java2"}
    ]
    
    # Processa todos os repositórios da lista
    process_multiple_repos(repo_list)
