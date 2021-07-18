import GetOldTweets3 as got

import pandas as pd

import snscrape.modules.twitter as sntwitter


def username_tweets_to_csv(username, count):
    # Creating list to append tweet data to
    tweets_list = []
    # ['Datetime', 'Text', 'UserName', 'URL', 'Retweets', 'Favorites', 'Quotes', 'Replies']
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('%s since:2005-01-01'%(username)).get_items()):
        print(i)
        print(tweet.id)
        tweets_list.append([tweet.date, tweet.content, tweet.user.username, tweet.url, tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.replyCount ])
        
    # Creating a dataframe from the tweets list above
    tweets_df2 = pd.DataFrame(tweets_list, columns=['Datetime', 'Text', 'UserName', 'URL', 'Retweets', 'Favorites', 'Quotes', 'Replies'])
    tweets_df2.to_csv('{}-2009-tweets.csv'.format(username), sep=',')

def batchScrapping(Array): 
    n = len(Array)
    count = 0 
    for i in range(n): 
        print(Array[i])
        username_tweets_to_csv(Array[i], count)

#username array consists of a list of twitter handle names
Array = ['#greenwash']
# Calling function to scrape all the pages specified in the array list
batchScrapping(Array)
		