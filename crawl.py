from bs4 import BeautifulSoup
import requests
import math
import time
r = requests.get(
    'http://steamcommunity.com/market/search/render?format=json/?query=&category_252490_itemclass[]=any&appid=252490&start=0&count=0')
response = r.json()
total_items = response['total_count']
count = 100
iterations = math.floor(total_items / count)
print(iterations)
with open("itemnames.txt", "w") as f:
    for i in range(0, iterations + 1):
        r = requests.get(
            'http://steamcommunity.com/market/search/render?format=json/?query=&category_252490_itemclass[]=any&appid=252490&start={0}&count={1}'.format(
                (i * count), count))
        response = r.json()
        # steamcommunity.com/market/search/render?format=json/?query=&category_252490_itemclass[]=any&appid=252490&start=0&count=100
        soup = BeautifulSoup(response['results_html'], 'html.parser')

        count = 0
        for item in soup.find_all("a", class_="market_listing_row_link"):
            item_soup = BeautifulSoup(str(item), 'html.parser')

            item_name = item_soup.find(
                "span", class_="market_listing_item_name").text
            f.write(item_name + '\n')
            count += 1
        print('Found {0} items'.format(count))
        print('Current iteration: {0} of {1}'.format(i, iterations + 1))
        print('Sleep for 1 min')
        time.sleep(30)
    f.close()
print("hi")
