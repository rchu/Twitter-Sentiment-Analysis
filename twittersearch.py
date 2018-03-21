import sys
from argparse import ArgumentParser
import tweepy
import pandas as pd
import numpy as np
import twittercredentials as tc 
from pathlib import Path
from time import sleep

def main():
	"""Parse command-line arguments and call twitter_search"""
	parser = ArgumentParser(
		description='Search Twitter and store the tweets in a file')
	parser.add_argument('q',
		metavar='query',
		help='Search query string')
	parser.add_argument('out',
		metavar='outfile.csv',
		help='CSV format file to save the search results.')
	parser.add_argument('--slow',
		action='store_true',
		help='Slow down to 1000 results per minute to avoid API time limits')

	args = parser.parse_args()

	twitter_search(**vars(args))

def twitter_search(q,out,slow):
	"""Performs a twitter API search using tweepy. lang=nl. Saves to a CSV file"""
	#
	#	Check if file exists and retreive since_id
	#
	since_id = 0
	out_dataframe = None

	if Path(out).exists():
		out_dataframe = pd.read_csv(out)
		since_id = out_dataframe['id'].max()

	print("newfile={} since_id={}".format(out_dataframe is None, since_id))

	#
	#	Connect to Twitter API
	#
	auth = tweepy.OAuthHandler(tc.consumer_key, tc.consumer_secret)
	auth.set_access_token(tc.access_token, tc.access_token_secret)
	api = tweepy.API(auth)

	#
	#	Search
	#
	results = []
	count=0
	count_printed=0
	print('Initiating Search', end='')
	try:
		for status in tweepy.Cursor(api.search, q=q, since_id=since_id, count=100, lang='nl').items():

			if hasattr(status,'retweeted_status'):
				rt = status.retweeted_status.id_str
			else:
				rt = ''

			try:	
				results.append(
					(int(status.id)
					,status.created_at
					,int(status.user.id)
					,status.user.name
					,status.text
					,status.lang
					,rt
					,int(status.favorite_count)
					,int(status.retweet_count)
					)
				)
			except ValueError:
				print('\nValueError parsing tweet:')
				print(status)

			count += 1
			if count - count_printed >= 100:
				print('\r{} tweets retrieved ({})'.format(count, status.created_at), end='')
				if slow:
					sleep((count-count_printed) * 0.06) #sleep 60 seconds per 1000 tweets
				count_printed = count

	except tweepy.TweepError as e:
		print('\rERROR: {}\n{} tweets retrieved'.format(e.reason,count))
	else:    
		print('\r{} tweets retrieved'.format(count))


	#
	#	Save results
	#

	results_dataframe = pd.DataFrame(
		data=results,
		columns=['id','date', 'user_id', 'user_name', 'text', 'lang', 'retweet','favorite_count', 'retweet_count'])

	if out_dataframe is None:
		print('Creating new DataFrame... ',end='')
		out_dataframe = results_dataframe
	else:
		print('Appending to DataFrame... ', end='')
		out_dataframe = out_dataframe.append(results_dataframe)

	out_dataframe.sort_values('id').to_csv(out,index=False, quoting=2) # 2 = QUOTE_NONNUMERIC 
	print('{} saved.'.format(out))

if __name__ == "__main__":
    main()