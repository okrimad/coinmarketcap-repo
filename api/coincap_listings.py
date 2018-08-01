import json
import requests    # pip3 install requests


listing_url = 'https://api.coinmarketcap.com/v2/listings/'

request = requests.get(listing_url)
results = request.json()

#print(json.dumps(results, sort_keys=True, indent=4))

data = results['data']

max_results = 50
i = 0
for currency in data:
  i += 1
  rank = currency['id']
  name = currency['name']
  symbol = currency['symbol']
  print(str(i) + ') ' + str(rank) + ': ' + name + ' (' + symbol + ')')
  if i == max_results:
    break