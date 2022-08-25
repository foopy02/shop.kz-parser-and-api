import json
import requests
import os
from os import path
from bs4 import BeautifulSoup

ROOT = f'{os.path.dirname(__file__)}/'
ROOT_OF_DATABASE = f'{os.path.dirname(__file__)}/smartphones.json'

class Product():
    def __init__(self, articul, name, price, memory_size):
        self.articul = articul
        self.name = name
        self.price = price
        self.memory_size = memory_size
    
    def save(self):
        def dump_db(db):
            with open(ROOT_OF_DATABASE, "w", encoding='utf-8') as f:
                json.dump(db, f, indent=2, ensure_ascii=False)
        
        if path.isfile(ROOT_OF_DATABASE):
            db = json.load(open(ROOT_OF_DATABASE, encoding='utf-8'))
            db.append(self.__dict__)
            dump_db(db)
        else:
            with open(ROOT_OF_DATABASE, "w", encoding='utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii=False)
            
            db = json.load(open(ROOT_OF_DATABASE, encoding='utf-8'))
            db.append(self.__dict__)
            dump_db(db)

class Parser():
    BASE_URL = "https://www.shop.kz"

    def get_content_of(self, url):
        headers ={
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate, lzma, sdch',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
        }
        print(f"Getting content of {url}")
        return requests.get(f'{url}',headers=headers).content
    
    def get_soup_of_url(self, url):
        return BeautifulSoup(self.get_content_of(url), "html.parser")
   
    def get_pages_numbers(self, soup_of_page):
        return int(soup_of_page.find("div", {'class': "bx-pagination-container row"}).find_all('a')[-2].text)

    def parse_page(self, soup_of_page):
        items = soup_of_page.find_all("div", {"class": "bx_catalog_item_container gtm-impression-product"})
        for item in items:
            product_info = json.loads(item.get("data-product"))
            #Getting memory info from title of product
            memory_size = product_info['item_name'].split(", ")[1].replace(" GB", "").replace("Gb", "")
            try:
                price = int(product_info['price'])
            except Exception as e:
                print(product_info)
                raise Exception(e)
            product = Product(
                articul=product_info["item_id"],
                name=product_info['item_name'].replace("Смартфон ", ""),
                price=int(product_info['price']),
                memory_size=f"{memory_size} Гб",
            )
            product.save()
    

def main():
    parser = Parser()
    target_category = f"{parser.BASE_URL}/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/"
    soup = parser.get_soup_of_url(target_category)
    #Getting pages numbers
    pages = parser.get_pages_numbers(soup_of_page=soup)
    for page in range(2, pages+1):
        target_page_url = f"{target_category}/?PAGEN_1={page}"
        soup = parser.get_soup_of_url(target_page_url)
        parser.parse_page(soup)
        

if __name__ == "__main__":
    main()
        