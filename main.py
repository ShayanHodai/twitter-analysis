#! /usr/bin/env python
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
Author: Shayan Hodai shayan.hodai@gmail.com
Date: 9 March 2023
Purpose: Scrape tweets from given accounts and do sentiment analysis
'''
import scrapper
import sentiment
import api

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
    tweets_and_sentiments = sentiment.do(all_tweets)
    api.initial(tweets_and_sentiments)


