from bs4 import BeautifulSoup
import requests
import time
import csv


def scrape_move_data(url_extension):
    # construct url from url extension
    full_url = f"https://pokemondb.net{url_extension}"

    # perform the get request to fetch the page content
    response = requests.get(full_url)

    # parse the response content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # find the move name, assuming it is the content in the
    move_name_h1 = soup.find('h1')
    # Strip " (move)" from the move name using replace
    move_name = move_name_h1.text.replace(' (move)', '').strip()

    description_p = soup.find('h2', string='Effects').find_next('p')
    description = description_p.text.strip() if description_p else 'No description found.'

    move_data_table = soup.find('table', class_='vitals-table')
    type_ = category = power = accuracy = pp = makes_contact= ""

    if move_data_table:
        rows = move_data_table.find_all('tr')
        for row in rows:
            header = row.find('th').text.strip() if row.find('th') else none
            value = row.find('td').text.strip() if row.find('td') else none
            if header == "Type":
                type_ = value
            elif header == "Category":
                category = value
            elif header == "Power":
                power = value
            elif header == "Accuracy":
                accuracy = value
            elif header == "PP":
                pp = value
            elif header == "Makes contact?":
                makes_contact = value

    return {
        'Name': move_name,
        'Description': description,
        'Type': type_,
        'Category': category,
        'Power': power,
        'Accuracy': accuracy,
        'PP': pp,
        'Makes Contact?': makes_contact
    }


base_url = "https://pokemondb.net/move/all"  # base url of abilitie page
page_to_scrape = requests.get(base_url)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

# collect all of a section of the html code
entries = soup.find_all('table', class_='data-table')[0].find_all('a')
url_extensions = []

for entry in entries:  # populates url extension list
    if entry and entry.has_attr('href') and entry['href'].startswith('/move'):
        url_extensions.append(entry['href'])

moves_data = []

#i = 1
for extension in url_extensions:
    #if i > 100:
     #   break
    move_data = scrape_move_data(extension)
    moves_data.append(move_data)
    #i += 1
    time.sleep(0.5)


with open('move_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Description', 'Type', 'Category',
                                              'Power', 'Accuracy', 'PP', 'Makes Contact?'])

    writer.writeheader()
    for data in moves_data:
        print(data)
        writer.writerow(data)
