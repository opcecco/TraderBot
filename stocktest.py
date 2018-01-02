#!/usr/bin/env python3

import sys, requests, json

result = requests.get('https://finance.google.com/finance', params = {'q': sys.argv[1], 'output': 'json'})

if result.status_code == 200:
	jobj = json.loads(result.text[6:-2])
	print('%s (%s)\nHigh: $%.2f\nLow: $%.2f\nLast price: $%.2f' % (jobj['name'], jobj['symbol'], float(jobj['hi'].replace(',', '')), float(jobj['lo'].replace(',', '')), float(jobj['l'].replace(',', ''))))
	
else:
	print('Failed to get stock info')
	