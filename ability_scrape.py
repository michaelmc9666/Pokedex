# I am aware that pokeapi exists and would make this process a lot easier.
# I am using this project as an opportunity to practice and display my web-scraping skills.
from bs4 import BeautifulSoup
import requests
import time


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


    # Return the data as a dictionary.
    return {
        'Num': str(ability_number),
        'Name': ability_name,           # returns data for dictionary
        'Desc': description
    }


base_url = "https://pokemondb.net/ability"  #base url of abilities page
page_to_scrape = requests.get(base_url)     # gets data from website
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
# collects all of a particular section of html code
entries = soup.find_all('table', class_='data-table')[0].find_all('a')

url_extensions = []                         # holds all the text to parse onto base url for individual pages

for entry in entries:                       # populates url_extensions list
    if entry and entry.has_attr('href') and entry['href'].startswith('/ability'):
        url_extensions.append(entry['href'])    # if the url is there, add it

abilities_data = []

i = 0
for extension in url_extensions:
    time.sleep(0.25)                         # pauses to give website a break
    ability_data = scrape_ability_data(extension, i)    # sets dictionary item to ability data
    abilities_data.append(ability_data)     # appends dictionary item to dictionary
    i += 1                                  # increments i for ability number

for data in abilities_data:
    print(data)                             # prints in order to test function
