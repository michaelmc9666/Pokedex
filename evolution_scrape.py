from bs4 import BeautifulSoup
import requests
import time
import csv

def scrape_evolution_data(block):
    # Initialize variables
    base_id, evolved_id, method = None, None, None

    # extracting the base pokemon details
    base_name_tag = block.find('a', class_='ent-name')
    base_id_tag = block.find('small')
    base_name = base_name_tag.text if base_name_tag else None
    base_id = base_id_tag.text.strip('#') if base_id_tag else None

    #extracting evolved pokemon details - assuming evolved is next infocad
    evolved_block = block.find_next('div', class_='infocard')
    evolved_name_tag = evolved_block.find('a', class_='ent-name') if evolved_block else None
    evolved_id_tag = evolved_block.find('small') if evolved_block else None
    evolved_id = evolved_id_tag.text.strip('#') if evolved_id_tag else None
    evolved_name = evolved_name_tag.text if evolved_name_tag else None

    # Extracting evolution method
    method_tag = block.find('span', class_='infocard-arrow').find_next('small')
    method = method_tag.next if method_tag else 'Unknown'

    return {'Base ID': base_id,
            'Base Name': base_name,
            'Evolved ID': evolved_id,
            'Evolved Name': evolved_name,
            'Method': method}

# url of page I am scraping
url = 'https://pokemondb.net/evolution'

# send get request to page
response = requests.get(url)

# parse the html content
soup = BeautifulSoup(response.text, 'html.parser')

# find all evolution blocks in the soup/html
evolution_blocks = soup.find_all('div', class_='infocard-list-evo')

evolution_data = []

for evolution_block in evolution_blocks:
    print(evolution_block)
    evolution_data.append(scrape_evolution_data(evolution_block))

#for data in evolution_data:
    #print(data)
    #print('\n')

    # writes it to a csv (must import to excel with utf-8)
with open('evolution_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Base ID', 'Base Name', 'Evolved ID', 'Evolved Name', 'Method'])
    writer.writeheader()
    for data in evolution_data:
        print(data)
        writer.writerow(data)



