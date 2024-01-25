# I am aware that pokeapi exists and would make this process a lot easier.
# I am using this project as an opportunity to practice and display my web-scraping skills.

from bs4 import BeautifulSoup
import requests
import time

base_url = "https://pokemondb.net/ability"  #base url of abilities page
page_to_scrape = requests.get(base_url)     # gets data from website
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
# collects all of a particular section of html code
entries = soup.find_all('table', class_='data-table')[0].find_all('a')

url_extensions = []

for entry in entries:
    time.sleep(0.5)                         # waiting, to be nice to website
    if entry and entry.has_attr('href') and entry['href'].startswith('/ability'):
        url_extensions.append(entry['href'])    # if the url is there, add it

for extension in url_extensions:
    print(extension)
