# Python code to use twitter api and feed data into Kinesis.
# This minimizes the amount of writes we do into Kinesis.
# Bulk write for each 100 records using put_records.

from TwitterAPI import TwitterAPI
import boto3
import json
import twitterCreds

# Twitter credentials.

consumer_key = twitterCreds.consumer_key
consumer_secret = twitterCreds.consumer_secret
access_token_key = twitterCreds.access_token_key
access_token_secret = twitterCreds.access_token_secret

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

kinesis = boto3.client('kinesis')

r = api.request('statuses/filter', {'locations':'-90,-90,90,90'})
tweets = []
count = 0
for item in r:
	jsonItem = json.dumps(item)
	# Dictionary included to allow us to put each record in bulk write to different shards in the stream.
	tweets.append({'Data':jsonItem, 'PartitionKey':"filler"})
	count += 1
	if count == 100:
		kinesis.put_records(StreamName="twitter", Records=tweets)
		count = 0
		tweets = []