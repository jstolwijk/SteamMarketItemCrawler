def clean_price(raw_price):
    raw_price = raw_price.replace('$', '')
    raw_price = raw_price.replace(' USD', '')
    return float(raw_price)
