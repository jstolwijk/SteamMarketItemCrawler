from bs4 import BeautifulSoup
import requests
import math
import time
import database
import pprint
db = database.connect()

rust = database.App.get_or_create(id=252490, name="Rust")


def getItemsByAppId(appId):
    BASE_URL = 'http://steamcommunity.com/market/search/render?format=json/?query=&category_{0}_itemclass[]=any&appid={0}&start={1}&count={2}'

    r = requests.get(BASE_URL.format(appId, 0, 0))
    response = r.json()

    total_items = response['total_count']
    count = 100
    iterations = math.floor(total_items / count)

    app_items = database.Item.select().where(database.Item.app == appId)
    print(len(app_items))
    with open("itemnames.txt", "w") as f:
        for i in range(0, iterations + 1):
            r = requests.get(
                BASE_URL.format(appId,
                                (i * count), count))
            response = r.json()
            soup = BeautifulSoup(response['results_html'], 'html.parser')

            count = 0
            for item in soup.find_all("a", class_="market_listing_row_link"):
                item_soup = BeautifulSoup(str(item), 'html.parser')

                item_name = item_soup.find(
                    "span", class_="market_listing_item_name").text

                price = item_soup.find("span", class_="sale_price").text
                print(price)
                f.write(item_name + '\n')
                count += 1
            print('Found {0} items'.format(count))
            print('Current iteration: {0} of {1}'.format(i, iterations + 1))
            print('Sleep for 30 sec')
            time.sleep(30)
        f.close()


import csv


def getItemTypes(appId):
    # BASE_URL = 'http://steamcommunity.com/market/search?appid={0}'

    # r = requests.get(BASE_URL.format(apppId))
    # response = r.text
    # print(response)
    # soup = BeautifulSoup(response, 'html.parser')
    # price = soup.find_all('select')
    # print(price)
    if appId == 252490:
        with open('tag_252490.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                database.Item.get_or_create(
                    app=rust[0].id, name=row[1], tag=row[0])


getItemsByAppId(252490)
getItemTypes(252490)
