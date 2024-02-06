from bs4 import BeautifulSoup
import requests
import time
import csv
import re


def scrape_move_data(url_extension):
    # construct url from url extension
    full_url = f"https://pokemondb.net{url_extension}"

    # perform the get request to fetch the page content
    response = requests.get(full_url)

    # parse the response content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # find the move name, assuming it is the content in the
    move_name_h1 = soup.find('h1')
    move_name = re.sub(r'\s*\([^)]*\)', '', move_name_h1.text).replace('move', '').strip()

    description_p = soup.find('h2', string='Effects').find_next('p')
    description = description_p.text.strip() if description_p else 'No description found.'

    move_type_th = soup.find('th', string='Type').find_next_sibling('td')
    move_type = move_type_th.get_text().strip() if move_type_th else 'Unknown'

    return {
        'Name': move_name,
        'Description': description,
        'Move_Type': move_type
    }


base_url = "https://pokemondb.net/move/all"      # base url of abilitie page
page_to_scrape = requests.get(base_url)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

# collect all of a section of the html code
entries = soup.find_all('table', class_='data-table')[0].find_all('a')
url_extensions = []

for entry in entries:       # populates url extension list
    if entry and entry.has_attr('href') and entry['href'].startswith('/move'):
        url_extensions.append(entry['href'])

moves_data = []

i = 1
for extension in url_extensions:
    if i>100:
        break
    time.sleep(0.5)
    move_data = scrape_move_data(extension)
    moves_data.append(move_data)
    i += 1

with open('move_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Description', 'Move_Type'])

    writer.writeheader()
    for data in moves_data:
        print(data)
        writer.writerow(data)