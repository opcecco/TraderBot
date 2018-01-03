#!/usr/bin/env python3

# Script to test out the unofficial Google Finance REST API
# It's surprisingly hard to find a free stock price API

# usage: python3 stocktest.py <symbol>

import sys, requests, json

# Querry
result = requests.get('https://finance.google.com/finance', params = {'q': sys.argv[1], 'output': 'json'})

if result.status_code == 200:

	# Returns malformed JSON, so we gotta snip it up to parse it properly
	parsable_text = result.text[6:-2]
	json_dict = json.loads(parsable_text)
	
	name = json_dict['name']
	symbol = json_dict['symbol']
	
	# Remove commas so we can parse as float
	daily_high = float(json_dict['hi'].replace(',', ''))
	daily_low = float(json_dict['lo'].replace(',', ''))
	last_price = float(json_dict['l'].replace(',', ''))
	
	print('%s (%s)\nHigh: $%.2f\nLow: $%.2f\nLast price: $%.2f' % (name, symbol, daily_high, daily_low, last_price))
	
else:
	print('Failed to get stock info')
	