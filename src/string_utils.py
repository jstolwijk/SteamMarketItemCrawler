def clean_price(raw_price):
    raw_price = raw_price.replace('$', '')
    raw_price = raw_price.replace(' USD', '')
    return float(raw_price)


def clean_url(raw_url):
    return raw_url.replace("/62fx62f", "")
