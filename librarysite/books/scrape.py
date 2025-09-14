from bs4 import BeautifulSoup
import requests
import re
from progress.bar import Bar
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "librarysite.settings")
django.setup()  

from books.models import Book, Category


page = 1
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
baseurl = "https://books.toscrape.com/catalogue/category/books_1/"

def InPage(soup):
    title = soup.find('h1').text
    imgurl = soup.find('img')['src']
    img = "https://books.toscrape.com/" + imgurl.replace('../../', '')
    genre_tags = soup.find_all('a', href=re.compile(r'^../category/books/'))
    genre_name = genre_tags[0].text if genre_tags else "Else"
    genre_obj, created = Category.objects.get_or_create(genre=genre_name)

    rating_class = soup.find('p', class_='star-rating')['class'][1]
    reviews = rating_map.get(rating_class, 0)

    content = (soup.find("div", id="product_description").find_next("p").text 
        if soup.find("div", id="product_description") else "No content")
    price_text = soup.find('p', class_='price_color').text
    price = float(price_text.replace('£', ''))
    availability = re.search(r"\d+", soup.find("th", string="Availability").find_next("td").text).group()
    reviews_count = soup.find("th", string="Number of reviews").find_next("td").text.strip()
    
    #! Books to Scrape has no "date" data
    #? Where to get the date?
    # This is value to fill a field in the database
    date = "2020-01-01"

    Book.objects.update_or_create(
        title=title,
        defaults={
            "img": img,
            "reviews": reviews,
            "content": content,
            "price": price,
            "availability": availability,
            "reviews_count": reviews_count,
            "genre": genre_obj,
            "date": date
        }
    )



with Bar('Saving', max=1000) as bar:
    for i in range(50):
        response = requests.get(baseurl + "page-" + str(page) + ".html")
        page = page + 1
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")

        links = [a['href'] for a in soup.select('article.product_pod div.image_container a')]

        for link in links:

            url = "https://books.toscrape.com/catalogue/" + link.replace('../../', '')

            book_response = requests.get(url)
            book_response.encoding = 'utf-8'
            book_soup = BeautifulSoup(book_response.text, 'lxml')
            
            InPage(book_soup)

            bar.next()
    
bar.finish()
