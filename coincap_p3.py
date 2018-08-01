##
##  Requirements:
##  $ source venv/bin/activate 
##  (venv)$ pip install prettytable colorama requests
##

import os
import json
import requests
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Back, Style


convert = 'USD'

global_url = 'https://api.coinmarketcap.com/v2/global/?convert=' + convert
url_end = '?structure=array&sort='

request = requests.get(global_url)
results = request.json()
data = results['data']

global_cap = int(data['quotes'][convert]['total_market_cap'])
global_cap_string = '{:,}'.format(global_cap)

# Infinite loop
while True:
  print()
  print("CoinMarket Cap Explorer Menu")
  print("The global market cap is $ " + global_cap_string)
  print()
  print("1 - Top 100 sorted by rank")
  print("2 - Top 100 sorted by 24 hour change")
  print("3 - Top 100 sorted by 24 hour volume")
  print("0 - Exit")
  print()
  choice = input("What is your choice? [1|2|3|0] => ")

  ticker_url = "https://api.coinmarketcap.com/v2/ticker/" + url_end

  if choice == '1':
    ticker_url += 'rank'
  elif choice == '2':
    ticker_url += 'percent_change_24h'
  elif choice == '3':
    ticker_url += 'volume_24h'
  elif choice == '0':
    break
  else:
    choice = input("Please choose [1|2|3|0] => ")

  request = requests.get(ticker_url)
  results = request.json()
  data = results['data']

  # Set table headers
  table = PrettyTable(['Rank', 'Asset', 'Price', 'Market Cap', 'Volume', '1h', '24h', '7d'])

  print()
  for currency in data:
    rank = currency['rank']
    name = currency['name']
    symbol = currency['symbol']
    quotes = currency['quotes'][convert]
    market_cap = quotes['market_cap']
    hour_change = quotes['percent_change_1h']
    day_change = quotes['percent_change_24h']
    week_change = quotes['percent_change_7d']
    price = quotes['price']
    volume = quotes['volume_24h']

    if hour_change is not None:
      if hour_change > 0:
        hour_change = Back.GREEN + str(hour_change) + ' %' + Style.RESET_ALL
      else:
        hour_change = Back.RED + str(hour_change) + ' %' + Style.RESET_ALL
    
    if day_change is not None:
      if day_change > 0:
        day_change = Back.GREEN + str(day_change) + ' %' + Style.RESET_ALL
      else:
        day_change = Back.RED + str(day_change) + ' %' + Style.RESET_ALL

    if week_change is not None:
      if week_change > 0:
        week_change = Back.GREEN + str(week_change) + ' %' + Style.RESET_ALL
      else:
        week_change = Back.RED + str(week_change) + ' %' + Style.RESET_ALL

    if volume is not None:
      volume_string = '{:,}'.format(volume)
    
    if market_cap is not None:
      market_cap_string = '{:,}'.format(market_cap)
    
    table.add_row([rank,
                   name + ' ( ' + symbol + ' )',
                   '$ ' + str(price),
                   '$ ' + str(market_cap),
                   '$ ' + str(volume),
                   str(hour_change),
                   str(day_change),
                   str(week_change)])

  print()
  print(table)
  print()

  choice = input("Again? [y/n] => ")
  choice = choice.lower()

  if choice == 'n':
    break