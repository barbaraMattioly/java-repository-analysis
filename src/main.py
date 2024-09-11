import requests
from dotenv import load_dotenv
import csv
import time
import os
from utils.utils import calculate_time_between_dates_in_days, format_date

load_dotenv('.env')

# Obtém o token do GitHub
personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')

# URL da API GraphQL do GitHub
github_graphQl_api_url = "https://api.github.com/graphql"

# Função para obter os repositórios mais populares com base no número de estrelas com paginação
def fetch_repos_data(num_repos):
    query = """
    query($number_of_repos_per_request: Int!, $cursor: String) {
        search(query: "language:Java stars:>0", type: REPOSITORY, first: $number_of_repos_per_request, after: $cursor)
        {
            edges {
                node {
                    ... on Repository {
                        name
                        url
                        stargazerCount
                        createdAt
                        releases {
                            totalCount
                        }
                    }
                }
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
    """
    
    repos = []
    cursor = None

    while len(repos) < num_repos:
        variables = {"number_of_repos_per_request": 20, "cursor": cursor}
        result = run_graphql_query(query, variables)
        edges = result["search"]["edges"]
        repos.extend(edges)
        
        if not result["search"]["pageInfo"]["hasNextPage"]:
            break
        
        cursor = result["search"]["pageInfo"]["endCursor"]

    # Ordenar repositórios por número de estrelas (decrescente) após a recuperação dos dados
    sorted_repos = sorted(repos, key=lambda r: r["node"]["stargazerCount"], reverse=True)

    return sorted_repos[:num_repos]

# Função para realizar chamada a API graphQL do Github para filtrar os repositórios
def run_graphql_query(query, variables=None):
    headers = {
        "Authorization": f"Bearer {personal_access_token}",
        "Content-Type": "application/json"
    }

    json = {"query": query, "variables": variables}

    retry_attempts = 3
    for attempt in range(retry_attempts):
        response = requests.post(github_graphQl_api_url, json=json, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if "errors" in result:
                raise Exception(f"Erro no GraphQL: {result['errors']}")
            return result["data"]
        elif response.status_code == 502 and attempt < retry_attempts - 1:
            print(f"Retrying due to 502 error (attempt {attempt + 1})...")
            time.sleep(3)  # Aguarda 3 segundos antes de tentar novamente
        else:
            raise Exception(f"Erro ao executar a query: {response.status_code}, {response.text}")

# Função para salvar informações dos repositórios em um arquivo .csv
def save_repo_info_to_csv(repos, filename):
    # Obtém o diretório onde o script está localizado
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, filename)
    
    # Define os cabeçalhos para o CSV
    headers = [
        "Index", "Nome do Repositório", "URL", "Total de Estrelas", "Data de Criação", "Idade do Repositório (anos)", "Total de Releases"
    ]

    # Abre o arquivo .csv para escrita
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Escreve os cabeçalhos no arquivo CSV

        # Escreve os dados dos repositórios no arquivo CSV
        for index, repo in enumerate(repos, start=1):
            repo_node = repo["node"]            
            repo_name = repo_node["name"]
            repo_url = repo_node["url"]
            repo_stars = repo_node["stargazerCount"]
            repo_creation_date = format_date(repo_node["createdAt"])
            repo_age_years = round(calculate_time_between_dates_in_days(repo_node["createdAt"]) / 365, 2)
            repo_number_of_releases = repo_node["releases"]["totalCount"]
            
            # Escreve os dados no arquivo CSV
            writer.writerow([
                index, repo_name, repo_url, repo_stars, repo_creation_date, repo_age_years,
                repo_number_of_releases
            ])

# Main
if __name__ == "__main__":
    number_of_repos = 1000 # Número de repositórios
    try:
        popular_repos = fetch_repos_data(number_of_repos)
        save_repo_info_to_csv(popular_repos, "repos_info.csv")
    except Exception as e:
        print(e)
