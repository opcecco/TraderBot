#!/usr/bin/env python3

import slackclient, time, argparse, websocket, yaml, os, sys
import traderbot


'''
Connect to a Slack team and start the bot
'''
def start_bot(config):
	
	client = slackclient.SlackClient(config['slack']['key'])
	timeout = config['slack']['delay']
	
	if not client.rtm_connect():
		print('Connection Failed')
		return
		
	# Get the bot's user ID to handle mentions
	bot_id = client.api_call("auth.test")["user_id"]
	print('Bot ID is: ' + bot_id)
	
	bot = traderbot.TraderBot()
	
	# Message listener loop
	while True:
		
		try:
			stream = client.rtm_read()
			print("Inside event loop")
			print("stream is:{}".format(stream))
			
			# Read all events in stream, react to user-entered messages only
			for event in stream:
				print("parsing an event")
				print("event is {}".format(event))
				if 'type' in event and 'channel' in event and 'text' in event and 'user' in event and event['type'] == 'message':
					
					channel = event['channel']
					user_id = event['user']
					
					# Get only ASCII characters for message text
					text = ''.join([c for c in event['text'] if 32 <= ord(c) <= 126])
					
					# Respond only if a user mentions the bot
					if bot_id in text:
						response = bot.respond(user_id, text)
						
						if response is not None:
							client.rtm_send_message(channel, response)
							
		# Sometimes we get text decode errors
		except UnicodeDecodeError:
			print('! Unicode Decode Error')
			
		# Attempt to reconnect if our bot loses connection
		except websocket.WebSocketConnectionClosedException:
			print('Attempting reconnect...')
			
			if not client.rtm_connect():
				print('! Failed')
			else:
				print('Success')
				
		# Delay the next listen loop
		time.sleep(timeout)
		
		
'''
Parse arguments and start a bot
'''
if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-c','--config',
			type = str,
			default = './config.yaml',
			help = 'Path to config file for the TraderBot')
	
	args = parser.parse_args()
	if not os.path.exists(args.config):
		parser.print_help()
		sys.exit(1)
	with open(args.config,'r') as f:
		config = yaml.load(f)
	start_bot(config)
	
