from bs4 import BeautifulSoup
import requests

def scrape_evolution_data(block):
    # initialize variables
    base_id, evolved_id, method = None, None, "Unknown"

    # extracting the base pokemon details
    base = block.find('span', class_='ent-name')
    print("Base element: ", base)

    if base:
        base_id = base.text.split("#")[1]
    else:
        print("Base element not found in block.")

    # extracting the evolved pokemon details
    evolved = block.find('a', class_='ent-name')
    print("Evolved block element: ")
    if evolved and "#" in evolved.text:
        evolved_id = evolved.text.split('#')[1]
    else:
        print("Evolved id not found in block.")

    # extracting evolution method. in same div
    method_container = block.find('div', class_='infocard-arrow')
    if method_container:
        method = block.find('div', class_='infocard-arrow').find_next_sibling(text=True).strip()
    else:
        print("Evolved method not found")

    return {'Base ID': base_id,
            'Evolved ID': evolved_id,
            'Method': method}

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
    evolution_data.append(scrape_evolution_data(evolution_block))

print(evolution_data)




