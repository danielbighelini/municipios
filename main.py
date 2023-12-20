import requests
from unidecode import unidecode
import pandas as pd
import csv


# Função para remover acentos de uma string
def remove_accented_chars(text):
    return unidecode(text)


# Lista de estados
estados = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']

# Lista de saida
datalist = []

for estado in estados:
    print(f"Consultando {estado}...")
    # URL da API do IBGE para listar municípios de um estado
    url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado}/municipios'

    # Faça a solicitação HTTP
    response = requests.get(url)

    # Verifique se a solicitação foi bem-sucedida (código 200)
    if response.status_code == 200:
        # Obtenha a lista de municípios em formato JSON
        municipios = response.json()

        # Exiba a lista de municípios
        for municipio in municipios:
            strlen = len(municipio['nome'])

            # Aplicar a função a cada nome de cidade
            municipio_noacc = remove_accented_chars(municipio['nome'])

            # consulta o estado do municipio
            estado = municipio.get('microrregiao', {}).get('mesorregiao', {}).get('UF', {}).get('sigla', '')

            # inclui em uma lista
            datalist.append({'id': municipio['id'], 'name': municipio['nome'], 'name_unac': municipio_noacc, 'state': estado})

    else:
        # Se a solicitação não for bem-sucedida, exiba o código de status
        print(f'Erro ao obter a lista de municípios. Código de status: {response.status_code}')

# Concatenar os dados em um DataFrame do pandas
df = pd.DataFrame(datalist)
# print(df)

# Nome do arquivo CSV
csv_file_path = 'municipios.csv'

# Exportar para CSV
df.to_csv(csv_file_path, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)
