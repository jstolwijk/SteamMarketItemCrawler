from bs4 import BeautifulSoup
import requests
import math
import time


def getItemsByAppId(appId):
    BASE_URL = 'http://steamcommunity.com/market/search/render?format=json/?query=&category_{0}_itemclass[]=any&appid={0}&start={1}&count={2}'

    r = requests.get(BASE_URL.format(appId, 0, 0))
    response = r.json()

    total_items = response['total_count']
    count = 100
    iterations = math.floor(total_items / count)

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


getItemsByAppId(252490)
