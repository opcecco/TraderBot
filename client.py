#!/usr/bin/env python3

import slackclient, time, argparse, websocket
import traderbot


'''
Connect to a Slack team and start the bot
'''
def start_bot(slack_token, listen_delay):
	
	client = slackclient.SlackClient(slack_token)
	
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
			
			# Read all events in stream, react to user-entered messages only
			for event in stream:
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
		time.sleep(listen_delay)
		
		
'''
Parse arguments and start a bot
'''
if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-d', '--delay',
		type = float,
		help = 'Time in seconds to wait between fetching messages',
		default = 0.5,
	)
	
	parser.add_argument('token',
		type = str,
		help = 'Slack token for connecting to a Slack team',
	)
	
	args = parser.parse_args()
	start_bot(args.token, args.delay)
	