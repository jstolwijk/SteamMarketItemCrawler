from bs4 import BeautifulSoup
import requests
import math
import time
import database
import csv
import string_utils
db = database.connect()

rust = database.App.get_or_create(id=252490, name="Rust")


def getItemSkins(app, item):

    BASE_URL = 'http://steamcommunity.com/market/search/render/?query=&category_{0}_itemclass[]={1}&appid={0}'
    ITERATOR_URL = BASE_URL.format(app.id, item.tag) + '&start={0}&count={1}'

    response = requests.get(ITERATOR_URL.format(0, 0)).json()

    total_items = response['total_count']
    count = 100
    iterations = math.floor(total_items / count)

    for i in range(0, iterations + 1):
        r = requests.get(
            ITERATOR_URL.format((i * count), count))
        response = r.json()
        soup = BeautifulSoup(response['results_html'], 'html.parser')

        count = 0
        for html_item in soup.find_all("a", class_="market_listing_row_link"):
            item_soup = BeautifulSoup(str(html_item), 'html.parser')

            item_name = item_soup.find(
                "span", class_="market_listing_item_name").text

            raw_price = item_soup.find("span", class_="sale_price").text
            price = string_utils.clean_price(raw_price)

            raw_thumbnail = item_soup.find("img")['src']
            thumbnail = string_utils.clean_url(raw_thumbnail)

            if len(database.Skin.select().where(database.Skin.name == item_name & database.Skin.item != item)) == 0:
                skin = database.Skin.get_or_create(
                    item=item, name=item_name, thumbnail=thumbnail)

                database.Price.create(
                    skin=skin[0], value=price, currency='USD')
            count += 1

        print('Found {0} items'.format(count))
        print('Current iteration: {0} of {1}'.format(
            i + 1, iterations + 1))
        print('Sleep for 30 sec')
        time.sleep(30)


def getItems(app):
    """
    TODO: use selenium to auto get items from the <select><option> tags
    BASE_URL = 'http://steamcommunity.com/market/search?appid={0}'
    """

    if app.id == 252490:
        with open('tag_252490.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                database.Item.get_or_create(
                    app=app.id, name=row[1], tag=row[0])


getItems(rust[0])

for item in database.Item.select():
    getItemSkins(rust[0], item)

# http://steamcommunity-a.akamaihd.net/economy/image/rtOnLXYSD-u65eusOk-nO4hCpUCJo2NbCxc2U4Y51MLNQ5Hz3URG1UJcBu0sv2Ko-M1Zj0mvYmKzVOblhE3kZTqDqzUUnSAYyUNwwYkIA2rnrMrfGSQK3vq1vQ/240fx240f
