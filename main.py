import requests
from bs4 import BeautifulSoup
import csv

en_tetes = ['product_page_url', "upc", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

# écriture de l'en-tête
def tete(name, en_tetes):

    with open(f"{name}.csv", "w", encoding=("utf-8")) as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(en_tetes)

# écriture des infos produit
def infos_produit(name, infos):

    with open(f"{name}.csv", "a", encoding=("utf-8")) as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(infos)



# récupération de la page produit
def product(url):
    
    # requête http page produit
    page_livre = requests.get(url)
    # objet BeautifulSoup
    soup = BeautifulSoup(page_livre.content, "html.parser")
    name = soup.find('li', class_='active').text

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

    return infos


def get_category_product(url_categorie, nom_categorie):
    
    """ Fonction qui récupère les infos de la page d'une catégorie du site http://books.toscrape.com/ à partir de son url
    ==> categorie('url de la page catégorie') """

    page_categorie = requests.get(url_categorie)
    soup = BeautifulSoup(page_categorie.content, "html.parser")
    page = 1
    # bouton 'next' en bas de page
    next_page = soup.find('li', class_ = "next")
    
    while next_page:
        url_categorie = url_categorie.replace('index.html', f'page-')

        # requête http catégorie
        page_categorie = requests.get(url_categorie + str(page) + ".html")
        # objet BeautifulSoup 
        soup = BeautifulSoup(page_categorie.content, "html.parser")

        # liste des urls des livres de la catégorie
        url_book = soup.find_all('li', class_= 'col-xs-6')
        liste_urls = []
        for u in url_book:
            liste_urls.append(u.find('a')['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))
            
        # extraction de plusieurs pages de la catégorie    
        # REECRIRE la boucle FOR CI-DESSOUS EN FONCTION
        for a in liste_urls:
            product_info = infos_livre(a)
            create_csv(nom_categorie, product_info)
        page += 1

        print(page)
        next_page = soup.find('li', class_ = "next")

    else: 
        # liste des urls des livres de la catégorie
        url_book = soup.find_all('li', class_= 'col-xs-6')
        liste_urls = []
        for u in url_book:
            liste_urls.append(u.find('a')['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))
        # extraction de la page de la catégorie
        # REECRIRE la boucle FOR CI-DESSOUS EN FONCTION
        for a in liste_urls:
            product_info = infos_livre(a)
            create_csv(nom_categorie, product_info)


def total(url = "https://books.toscrape.com/index.html"):

    # requête http
    url_total = requests.get(url)
    print(url_total.status_code)

    # objet BeautifulSoup
    soup = BeautifulSoup(url_total.content, "html.parser")

    # récupération de toutes les urls des catégories des livres dans une liste
    categories = soup.find('ul', class_= 'nav-list').find_all('a')
    liste_categories = []
    for categorie in categories[1:]:
        url_categorie = "https://books.toscrape.com/" + categorie["href"]
        nom_categorie = categorie.text.strip()
        get_category_product(url_categorie, nom_categorie)
        # liste_categories.append("https://books.toscrape.com/" + l["href"])
    
    # récupération des noms des catégories dans une liste
    noms_categories = []
    for name in categories[1:]:
        noms_categories.append(name.text.strip())


get_category_product("https://books.toscrape.com/catalogue/category/books/mystery_3/index.html", "Mystery")
