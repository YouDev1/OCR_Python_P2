import requests
from bs4 import BeautifulSoup
import csv

# liste des en-têtes
en_tetes = ['product_page_url', "upc", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

# écriture de l'en-tête

with open("TEST.csv", "w", encoding=("utf-8")) as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(en_tetes)


# écriture des informations
def inf(infos):     
    with open("TEST.csv", 'a', encoding=("utf-8")) as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(infos)

# récupération de la page produit
def infos_livre(url = "http://books.toscrape.com/catalogue/the-10-entrepreneur-live-your-startup-dream-without-quitting-your-day-job_836/index.html"): 

    """ Fonction qui récupère les infos de la page d'un livre du site http://books.toscrape.com/ à partir de son url
    ==> infos_livre('url de la page du livre') """

    # requête http page produit
    page_livre = requests.get(url)

    # objet BeautifulSoup
    soup = BeautifulSoup(page_livre.content, "html.parser")

    table = soup.find('table').find_all('td')

    # affectation des différentes variables du livre
    product_page_url = page_livre.url
    upc = table[0]
    title = soup.find('h1')
    price_including_tax = table[3]
    price_excluding_tax = table[2]
    number_available = table[5]
    product_description = soup.select_one('article').select('p')[3]
    category = soup.find('ul', class_ = 'breadcrumb').find_all('li')[2]
    review_rating = table[-1]
    image_url = soup.select_one("#product_gallery").find('img')['src']

    # liste des infos du livre
    infos = [product_page_url, upc.text, title.text, price_including_tax.text, price_excluding_tax.text, number_available.text, product_description.text, category.text, review_rating.text, image_url.replace('../..', 'http://books.toscrape.com')]

    # écriture des données dans un fichier csv 
    inf(infos)