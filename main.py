from bs4 import BeautifulSoup
import requests
import csv

page_to_scrape = requests.get("https://pokemondb.net/pokedex/national")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

names = []              # creating a list for pokemon names
numbers = []            # creating a list for pokemon numbers

entries = soup.find_all('span', class_='infocard-lg-data text-muted')
                        # this list holds all instance of pokemon and numbers

for entry in entries:   # goes through each entry and extracts name and number
    #number is in small tag, formatted like #0001
    number_tag = entry.find('small')
    if number_tag:      # checks if it exists before appending to the list
        numbers.append(number_tag.text)
    else:
        numbers.append('Number not found')


    #name is in the 'a' tag with the class 'ent-name'
    name_tag = entry.find('a', class_='ent-name')
    if name_tag:        # checks if it exists before appending to the list
        names.append(name_tag.text)
    else:
        names.append('Name not found')

#opens a new csv files to write to
with open('pokemon_data.csv', 'w', newline='', encoding='utf-8') as file:
    #creates a writer object
    writer = csv.writer(file)

    #writes a single row to the csv files, for the header
    writer.writerow(['Number', 'Name'])

    #creates loop to iterate over names and numbers and add to the file
    for name, number in zip(names, numbers):
        writer.writerow([number, name])
