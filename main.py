#! /usr/bin/env python
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import scrapper
import sentiment

import time
start_time = time.time()

accounts = ['elonmusk', 'ylecun', 'BarackObama'] #accounts which we want to scrape tweets from

if __name__ == '__main__':
    tweets_df = scrapper.tweets(accounts)
    threads_df = scrapper.threads(accounts, tweets_df)
    replies_df = scrapper.replies(accounts, tweets_df)
    replies_df = scrapper.rm_dup(threads_df['Thread'], replies_df)
    all_tweets = scrapper.merge_dfs(tweets_df, threads_df, replies_df)
    all_tweets = scrapper.preprocess(all_tweets)
    #tweets_and_sentiments = sentiment.do(all_tweets)
    #print(tweets_and_sentiments.head())
    print(all_tweets)
    print('time it took:{0}'.format(time.time()-start_time))

