from bs4 import BeautifulSoup
import requests
import csv

page_to_scrape = requests.get("https://pokemondb.net/pokedex/national")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

base_url = "https://pokemondb.net"
url_extensions = []                                         # list for pokemon url extensions
pokemon_data = []

entries = soup.find_all('span', class_='infocard-lg-data text-muted')
                                                            # this list holds all instances of pokemon information

for entry in entries:                                       # goes through each entry and extracts url extension
    url_tag = entry.find('a', class_='ent-name')
    if url_tag and url_tag.has_attr('href'):
        url_extensions.append(url_tag['href'])              # appends the href attribute (url extension)

for extension in url_extensions:
    full_url = base_url + extension
    page = requests.get(full_url)                           # fetches html content of webpage using get request
    soup = BeautifulSoup(page.text, "html.parser")  # parses html content info readable format

    #extract the desired data from each pokemon
    name = soup.find('h1').text
    type_tags = soup.find_all('a', class_='type-icon')
    type1 = type_tags[0].text if type_tags else 'null'      # extracts all data from soup
    type2 = type_tags[1].text if len(type_tags) > 1 else 'null'
    height = soup.find('th', string='Height').find_next_sibling('td').text
    weight = soup.find('th', string='Weight').find_next_sibling('td').text

                                                            # appends all the data to the pokemon_data list
    pokemon_data.append({
        'Name': name,
        'Type1': type1,
        'Type2': type2,
        'Height': height,
        'Weight': weight
    })
                                                            # writes it to a csv (must import to excel with utf-8)
with open('pokemon_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Type1', 'Type2', 'Height', 'Weight'])
    writer.writeheader()
    for data in pokemon_data:
        writer.writerow(data)




