##
##  Requirements:
##  VBox => Core Audio ICH AC97
##  Ubuntu Text To Speech:
##  apt-get install gnustep-gui-runtime
##  
##  $ source venv/bin/activate
##

import os
import json
import requests
import time
from datetime import datetime


convert = 'USD'

listings_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
url_end = '?structure=array&convert=' + convert

request = requests.get(listings_url)
results = request.json()
data = results['data']

# Dictionary => key : value
ticker_url_pairs = {}
for currency in data:
  symbol = currency['symbol']
  url = currency['id']
  ticker_url_pairs[symbol] = url

print()
print("ALERTS TRACKING...")
print()

already_hit_symbols = []

# Infinite loop
while True:

  # Read text file
  with open("alerts.txt") as inp:
    for line in inp:
      # Store into 2 vars strings before and after space
      ticker, amount = line.split()
      ticker = ticker.upper()
    
      # Call API
      ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end
      request = requests.get(ticker_url)
      results = request.json()

      currency = results['data'][0]
      name = currency['name']
      last_updated = currency['last_updated']
      symbol = currency['symbol']
      quotes = currency['quotes'][convert]
      price = quotes['price']

      if (float(price) >= float(amount)) and (symbol not in already_hit_symbols):
        os.system('sudo say ' + name + ' hit ' + amount)
        last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')
        print(name + ' hit ' + amount + ' on ' + last_updated_string)
        already_hit_symbols.append(symbol)

  print("...")
  time.sleep(300)