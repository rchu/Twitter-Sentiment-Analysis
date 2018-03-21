# Twitter sentiment analysis

## Downloading tweets
The [script](twittersearch.py) uses [Tweepy](http://tweepy.readthedocs.org/) to search for a query string (and limits results to lang='nl'). It uses `twittercredentials.py` (not included) which contains four variables: `consumer_key`, `consumer_secret`, `access_token` and `access_token_secret` to authenticate with the Twitter API.

Results are stored in a CSV file and if that output file already exists it will update that file with tweets newer than the latest tweet in the file.

## Sentiment analysis
I use [pattern](https://www.clips.uantwerpen.be/pages/pattern) for Dutch sentiment analysis. This is done in a seperate [script](sentiment-analysis.py) since pattern does not work with python 3. 

