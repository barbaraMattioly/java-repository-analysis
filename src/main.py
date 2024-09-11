import requests
from dotenv import load_dotenv
import csv
import os
from utils.utils import calculate_time_between_dates_in_days, format_date

load_dotenv('.env')

# Obtém o token do GitHub
personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')

# URL da API GraphQL do GitHub
github_graphQl_api_url = "https://api.github.com/graphql" 

# Nome do arquivo TXT para persistir os dados
txt_filename = 'extracted_data.txt'

# Consulta GraphQL
def build_query(number_of_repos, after_cursor=None):
    after_clause = f', after: "{after_cursor}"' if after_cursor else ''
    return f"""
    {{
        search(
            type: REPOSITORY,
            first: {number_of_repos}
            query: "language:Java stars:>0"{after_clause}
        ) {{
            edges {{
                cursor
                node {{
                    ... on Repository {{
                        name
                        url
                        stargazerCount
                        createdAt
                        releases {{
                            totalCount
                        }}
                        object(expression: "HEAD:") {{
                            ... on Tree {{
                                entries {{
                                    name
                                    type
                                    object {{
                                        ... on Blob {{
                                            text
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
            pageInfo {{
                endCursor
                hasNextPage
            }}
        }}
    }}
    """

# Função para realizar chamada a API do Github para filtrar os repositórios
def fetch_repos_data(number_of_repos):
    # Cabeçalhos da requisição
    headers = {
        "Authorization": f"Bearer {personal_access_token}",
        "Content-Type": "application/json"
    }

    number_of_repos_per_request = 10
    has_next_page = True
    after_cursor = None
    all_repositories = []

    while has_next_page and len(all_repositories) < number_of_repos:
        query = build_query(min(number_of_repos_per_request, number_of_repos - len(all_repositories)), after_cursor)
        response = requests.post(github_graphQl_api_url, json={'query': query}, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            all_repositories.extend(result['data']['search']['edges'])
            has_next_page = result['data']['search']['pageInfo']['hasNextPage']
            after_cursor = result['data']['search']['pageInfo']['endCursor']
        else:
            raise Exception(f"Failed to fetch repositories: {response.status_code}")

    return all_repositories

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
    number_of_repos = 10  # Número de repositórios
    try:
        popular_repos = fetch_repos_data(number_of_repos)
        save_repo_info_to_csv(popular_repos, "repos_info.csv")
    except Exception as e:
        print(e)
