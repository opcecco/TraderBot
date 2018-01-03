#!/usr/bin/env python3


class TraderBot:
	
	def __init__(self):
		# TODO: Load portfolio info from cache file
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
		
		return 'Hello <@%s>' % user_id
		