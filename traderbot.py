#!/usr/bin/env python3
import requests,json


class TraderBot:
	
	members = {}
	api_key = ""
	api_endpoint = ""
	def __init__(self,config,users):
		# TODO: Load portfolio info from cache file
		self.api_key = config['alpha_vantage']['key']
		self.api_endpoint = config['alpha_vantage']['endpoint']
		if users['ok']:
			for user in users['members']:
				self.members[user['name']] = user['id']
		pass
		
		
	def respond(self, user_id, message):
		# TODO: Parse message, get stock info, adjust portfolio
		
		# Commands to add:
		#	buy:	buy some shares
		#	sell:	sell some shares
		#	info:	print basic stock info
		
		# Message examples:
		#	@TraderBot buy 25 AAPL
		#	@TraderBot sell 12 GOOG
		#	@TraderBot info BABA
		print("Message is {}".format(message))
		msg_split = message.split(" ")[1:]
		if msg_split and msg_split[0] == "list":
			ret = ""
			for member in self.members:
				ret += "{}:{}\n".format(member,self.members[member])
			return ret
		elif msg_split and msg_split[0] == "quote" and len(msg_split) > 1:
			return self.lookup_stock(msg_split[1])

		elif msg_split and msg_split[0] != '<@U8NE8SSET>':
			return 'Hello <@%s>' % user_id
	
	def lookup_stock(self,symbol):
		request_data = {}
		tseries = "5min"
		request_data['function'] = "TIME_SERIES_INTRADAY"
		request_data['symbol'] = symbol
		request_data['interval'] = tseries
		request_data['apikey'] = self.api_key
		request = requests.get(self.api_endpoint,params=request_data)
		response = json.loads(request.text)
		quotes = response['Time Series ({})'.format(tseries)]
		return "quotes for {} are {}".format(symbol,quotes)
		

		
