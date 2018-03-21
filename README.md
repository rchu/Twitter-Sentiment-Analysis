# Twitter sentiment analysis

## Downloading tweets
The script `twittersearch.py` uses [Tweepy](http://tweepy.readthedocs.org/) to search for a query string. Returns all results with lang='nl' as far back as the API allows.

Results are stored in a CSV file and if that output file already exists it will update that file with tweets newer than the latest tweet in the file.

## Sentiment analysis
I use [pattern](https://www.clips.uantwerpen.be/pages/pattern) for Dutch sentiment analysis. This is done in a seperate python 2 script `sentiment-analysis` since pattern does not work with python 3

I've included a little [Jupyter notebook](sentiment-analysis.ipynb) that visualizes sentiment on tweets about "wilders" (because Geert Wilders is always a fun example)