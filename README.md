# java-repository-analysis

# 📈 Um estudo das características de qualidade de sistema java - [Lab02]

💻Laboratório de Experimentação de Software 

Esse projeto tem como objetivo analisar aspectos da qualidade de repositórios desenvolvidos na linguagem Java, correlacionando-os com características do seu processo de desenvolvimento, sob a perspectiva de métricas de produto calculadas através da ferramenta CK.

**Questões de Pesquisa:**

**RQ 01**. Qual a relação entre a popularidade dos repositórios e as suas características de
qualidade?

**RQ 02.** Qual a relação entre a maturidade do repositórios e as suas características de
qualidade ?

**RQ 03.** Qual a relação entre a atividade dos repositórios e as suas características de
qualidade?

**RQ 04.** Qual a relação entre o tamanho dos repositórios e as suas características de
qualidade? 


**Definições de métricas**
Para cada questão de pesquisa, realizaremos a comparação entre as características do
processo de desenvolvimento dos repositórios e os valores obtidos para as métricas
definidas nesta seção. Para as métricas de processo, define-se:
• Popularidade: número de estrelas
• Tamanho: linhas de código (LOC) e linhas de comentários
• Atividade: número de releases
• Maturidade: idade (em anos) de cada repositório coletado

Por métricas de qualidade, entende-se:
• CBO: Coupling between objects
• DIT: Depth Inheritance Tree
• LCOM: Lack of Cohesion of Methods


## 👩🏻‍💻 Alunos:
* Bárbara Mattioly Andrade  
* Laura Enísia Rodrigues Melo
* Samuel Marques Sousa Leal 
 
## 👨‍🏫 Professor:
* João Paulo Carneiro Aramuni

## 💻 Para compilação e execução do sistema:
1. Clone o repositório do projeto;
2. Crie um arquivo .env com a mesma estrutura e no mesmo nível do .env.example. Em seguida gere um token de acesso do github e substitua o PERSONAL_ACCESS_TOKEN.
3. Instale as dependências das bibliotecas usadas como `pip install requests python-dotenv python-dateutil`.
4. Execute o arquivo `main.py`

## 📝 Sobre o projeto:
- O arquivo **main.py** possui as funções principais para executar a consulta em GraphQL, extrair os dados relevantes para o sistema e coletar as informações salvando no arquivo  'repos_info.csv'
