from bs4 import BeautifulSoup
import requests
import csv
import time
import re

page_to_scrape = requests.get("https://pokemondb.net/pokedex/national")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

base_url = "https://pokemondb.net"
url_extensions = []  # list for pokemon url extensions
pokemon_data = []  # this list holds all instances of pokemon information

entries = soup.find_all('span', class_='infocard-lg-data text-muted')

counter = 0  # only doing the 1st 100 pokemon while testing
max_pokemon = 1000
for entry in entries:  # goes through each entry and extracts url extension
    if counter >= max_pokemon:  # limited testing run break statement
        break

    url_tag = entry.find('a', class_='ent-name')
    if url_tag and url_tag.has_attr('href'):
        url_extensions.append(url_tag['href'])  # appends the href attribute (url extension)
        counter += 1  # counter for limited testing runs

for extension in url_extensions:
    full_url = base_url + extension
    #time.sleep(0.25)  # sleeps 1 second between queries to respect website
    page = requests.get(full_url)  # fetches html content of webpage using get request
    soup = BeautifulSoup(page.text, "html.parser")  # parses html content info readable format

    # extract the desired data from each pokemon
    number_th = soup.find('th', string='National №')
    number = number_th.find_next_sibling('td').text if number_th else 'null'

    name = soup.find('h1').text

    species_th = soup.find('th', string=re.compile(r'Species'))
    species = species_th.find_next_sibling('td').get_text(strip=True) if species_th else 'null'

    type_tags = soup.find_all('a', class_='type-icon')
    type1 = type_tags[0].text if type_tags else 'null'  # extracts all data from soup
    type2 = type_tags[1].text if len(type_tags) > 1 else 'null'

    height = soup.find('th', string='Height').find_next_sibling('td').text
    weight = soup.find('th', string='Weight').find_next_sibling('td').text

    hp_th = soup.find('th', string='HP')
    hp = hp_th.find_next_sibling('td').text if hp_th else 'null'

    attack_th = soup.find('th', string='Attack')
    attack = attack_th.find_next_sibling('td').text if attack_th else 'null'

    defense_th = soup.find('th', string='Defense')
    defense = defense_th.find_next_sibling('td').text if defense_th else 'null'

    sp_atk_th = soup.find('th', string='Sp. Atk')
    sp_attack = sp_atk_th.find_next_sibling('td').text if sp_atk_th else 'null'

    sp_def_th =    soup.find('th', string='Sp. Def')
    sp_defense =   sp_def_th.find_next_sibling('td').text if sp_def_th else 'null'

    speed_th =     soup.find('th', string='Speed')
    speed =        speed_th.find_next_sibling('td').text if speed_th else 'null'

    total_th =     soup.find('th', string='Total')
    total =        total_th.find_next_sibling('td').text if total_th else 'null'

    # appends all the data to the pokemon_data list
    pokemon_data.append({
        'Number': number.zfill(4),
        'Name': name,
        'Species': species,
        'Type 1': type1,
        'Type 2': type2,
        'Height': height,
        'Weight': weight,
        'HP': hp,
        'Attack': attack,
        'Defense': defense,
        'Sp. Attack': sp_attack,
        'Sp. Defense': sp_defense,
        'Speed': speed,
        'Total': total
    })
    # writes it to a csv (must import to excel with utf-8)
with open('pokemon_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Number', 'Name', 'Species', 'Type 1', 'Type 2', 'Height', 'Weight', 'HP',
                                              'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed', 'Total'])
    writer.writeheader()
    for data in pokemon_data:
        writer.writerow(data)
