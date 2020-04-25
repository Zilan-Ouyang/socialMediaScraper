import GetOldTweets3 as got
import pandas as pd

def username_tweets_to_csv(username, count):
    # Creation of query object
    tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                                            .setSince('2012-01-01')

                                            #.setSince('2018-01-01') #.setUntil('2019-01-01').setTopTweets(True).setMaxTweets(10000) #

                                            #.setSince('2015-01-01').setUntil('2018-01-01') #.setTopTweets(True).setMaxTweets(8000) #.setUntil('2017-12-31')

                                            #.setSince('2012-01-01').setUntil('2015-01-01')








                                            #.setSince('2015-12-01').setUntil('2015-12-31').setTopTweets(True).setMaxTweets(1000)
                                            #.setSince('2016-01-01').setUntil('2016-12-31')
                                            #
                                            #.setUntil('2014-12-31')
                                            #
                                            #.setSince('2017-01-01').setUntil('2018-12-31')
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    # Creating list of chosen tweet data
    user_tweets = [[tweet.date, tweet.text, tweet.permalink,tweet.retweets,tweet.favorites] for tweet in tweets]
    #user_tweets = [[tweet.date, tweet.text] for tweet in tweets]
    #user_tweets = [[tweet.date, tweet.permalink] for tweet in tweets]
    #user_tweets = [[tweet.date, tweet.retweets] for tweet in tweets]
    #user_tweets = [[tweet.date, tweet.favourites] for tweet in tweets]
    

    # Creation of dataframe from tweets list
    tweets_df = pd.DataFrame(user_tweets, columns = ['Datetime', 'Text', 'URL', 'Retweets', 'Favorites'])
    #tweets_df = pd.DataFrame(user_tweets, columns = ['Datetime', 'Text'])
    #tweets_df = pd.DataFrame(user_tweets, columns = ['Datetime', 'Url'])
    #tweets_df = pd.DataFrame(user_tweets, columns = ['Datetime', 'Retweets'])
    #tweets_df = pd.DataFrame(user_tweets, columns = ['Datetime', 'Favourites'])
    

    # Converting dataframe to CSV
    #tweets_df.to_csv('{}-2012-2014-tweets.csv'.format(username), sep=',')
    #tweets_df.to_csv('{}-2015-2017-tweets.csv'.format(username), sep=',')
    #tweets_df.to_csv('{}-2018-now-tweets.csv'.format(username), sep=',')
    #tweets_df.to_csv('{}-2018-tweets.csv'.format(username, int(count/1000)), sep=',')
    tweets_df.to_csv('{}-all-tweets.csv'.format(username), sep=',')
    #tweets_df.to_csv('{}-{}k-tweets-favourites.csv'.format(username, int(count/1000)), sep=',')
def batchScrapping(Array): 
    n = len(Array)
    count = 0 
    for i in range(n): 
        print(Array[i])
        username_tweets_to_csv(Array[i], count)

#username = 'Shell_NatGas'
#count = 5000  HyundaiIndia 2016, 2017 2012-2014 Kia
Array = ['Total'] #,,'','','',''Total]
#''
#'' 
#'' 				 				
#''
#''
#'' 
#'', 
#                      
# '','''''','','','','','',''
batchScrapping(Array)
# Calling function to turn username's past x amount of tweets into a CSV file		
#				
#	
# 			
#				
#				
#				
#				
#				
				
#				
#				
#			