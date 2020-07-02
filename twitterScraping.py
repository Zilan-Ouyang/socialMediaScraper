import GetOldTweets3 as got
import pandas as pd

def username_tweets_to_csv(username, count):
    # Creation of query object
    tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                                            .setSince('2012-01-01')
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    # Creating list of chosen tweet data
    user_tweets = [[tweet.date, tweet.text, tweet.permalink,tweet.retweets,tweet.favorites] for tweet in tweets]
    # Creation of dataframe from tweets list
    tweets_df = pd.DataFrame(user_tweets, columns = ['Datetime', 'Text', 'URL', 'Retweets', 'Favorites'])
    # Converting dataframe to CSV
    tweets_df.to_csv('{}-all-tweets.csv'.format(username), sep=',')

def batchScrapping(Array): 
    n = len(Array)
    count = 0 
    for i in range(n): 
        print(Array[i])
        username_tweets_to_csv(Array[i], count)

#username array consists of a list of twitter handle names
Array = ['Total', 'shell']
# Calling function to scrape all the pages specified in the array list
batchScrapping(Array)
		