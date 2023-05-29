import requests
from bs4 import BeautifulSoup

# define the URL of the website to scrape
url = 'https://english.onlinekhabar.com/'

# send a GET request to the website
response = requests.get(url)

# check if the request was successful
if response.status_code == 200:
    # parse the HTML content of the website using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # extract the text content of the website
    website_text = soup.get_text()

    #website_text = ' '.join(website_text.split())

    # print the text content of the website
    print(website_text)

    with open('website_text.txt', 'w', encoding='utf-8') as f:
        f.write(website_text)
else:
    print('Error:', response.status_code)
