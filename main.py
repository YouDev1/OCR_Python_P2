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