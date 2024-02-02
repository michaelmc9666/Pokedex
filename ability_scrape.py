# I am aware that pokeapi exists and would make this process a lot easier.
# I am using this project as an opportunity to practice and display my web-scraping skills.
from bs4 import BeautifulSoup
import requests
import time
import csv


def read_pokemon_numbers():
    pokemon_numbers = {}
    # open the pokemon data csv file
    with open('pokemon_data.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # creates a dictionary mapping pokemon names to their numbers
        for row in reader:
            pokemon_numbers[row['Name']] = row['Number']
        return pokemon_numbers


# Function to scrape ability details based on the URL extension.
def scrape_ability_data(url_extension, ability_number):
    # Constructing the full URL from the base URL and the extension.
    full_url = f"https://pokemondb.net{url_extension}"

    # Perform the GET request to fetch the page content.
    response = requests.get(full_url)

    # Parse the response content with BeautifulSoup.
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the ability name, assuming it is the content of the first h1 tag.
    ability_name_h1 = soup.find('h1')
    ability_name = ability_name_h1.text.replace('(ability)', '').strip()

    # Find the description, assuming it is the content of the first p tag after the h2 tag with 'Effect'.
    description_p = soup.find('h2', string='Effect').find_next('p')
    description = description_p.text.strip() if description_p else 'No description found.'

    # find the section listing with pokemon with that ability
    pokemon_table = soup.find('table', class_='data-table')
    #print(pokemon_table)
    # initialize an empty list for pokemon numbers
    pokemon_nums = []

    # only proceed if the section exists
    if pokemon_table:
        # extract all rows in the table
        pokemon_rows = pokemon_table.find_all('tr')
        for row in pokemon_rows:
            # find pokemon name cell
            cell = row.find('td', class_='cell-name')
            if cell and cell.find('a'):
                #extract pokemon name
                pokemon_name = cell.find('a').text


                #convert pokemon name to number with previous dictionary
                pokemon_num = pokemon_numbers.get(pokemon_name, 'unknown')
                if pokemon_num != 'unknown':
                    pokemon_nums.append(pokemon_num)



    # Return the data as a dictionary.
    return {
        'Number': str(ability_number),
        'Name': ability_name,  # returns data for dictionary
        'Description': description,
        'PokemonNumbers': pokemon_nums
    }


base_url = "https://pokemondb.net/ability"  # base url of abilities page
page_to_scrape = requests.get(base_url)  # gets data from website
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
# collects all of a particular section of html code
entries = soup.find_all('table', class_='data-table')[0].find_all('a')

pokemon_numbers = read_pokemon_numbers()  # creates dictionary for pokemon number lookup
url_extensions = []  # holds all the text to parse onto base url for individual pages

for entry in entries:  # populates url_extensions list
    if entry and entry.has_attr('href') and entry['href'].startswith('/ability'):
        url_extensions.append(entry['href'])  # if the url is there, add it

abilities_data = []

i = 1
for extension in url_extensions:
    #if i > 100:    # limited scraping for testing
     #   break
    time.sleep(1)  # pauses to give website a break
    ability_data = scrape_ability_data(extension, i)  # sets dictionary item to ability data
    abilities_data.append(ability_data)  # appends dictionary item to dictionary
    i += 1  # increments i for ability number

with open('ability_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Number', 'Name', 'Description', 'PokemonNumbers'])
    writer.writeheader()
    for data in abilities_data:
        #print(data)
        data['PokemonNumbers'] = ','.join(data['PokemonNumbers'])
        print(data['PokemonNumbers'])
        writer.writerow(data)

