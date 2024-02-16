from bs4 import BeautifulSoup
import requests

def scrape_evolution_data(block):
    base = block.find('span', class_='ent-name')
    base_pokemon_id = base.text.split("#")[1]

    evolved = block.find('small')

# url of page I am scraping
url = 'https://pokemondb.net/evolution'

# send get request to page
response = requests.get(url)

# parse the html content
soup = BeautifulSoup(response.text, 'html.parser')

# find all evolution blocks in the soup/html
evolution_blocks = soup.find_all('div', class_='infocard')

evolution_data = []

for evolution_block in evolution_blocks:
    evolution_data.append(evolution_block)




