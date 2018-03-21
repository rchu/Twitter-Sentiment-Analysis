"""Performs sentiment analysis on a twitter search result dataset.
In dutch, using pattern https://www.clips.uantwerpen.be/pages/pattern (python2))"""

import pandas as pd
from pattern.nl import sentiment
from matplotlib import pyplot as plt
from sys import argv

if len(argv) != 3:
    print('USAGE: '+argv[0]+' <infile> <outfile>')
else:

    def sentiment_function(row):
        row['polarity'], row['subjectivity'] = sentiment(row['text'])
        return row

    df = pd.read_csv(argv[1], parse_dates=['date'])
    df = df.apply(sentiment_function, axis=1)
    df.to_csv(argv[2])