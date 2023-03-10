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

accounts = ['elonmusk', 'ylecun', 'BarackObama'] #accounts which we want to scrape tweets from

if __name__ == '__main__':
    tweets_df = scrapper.tweets(accounts) #scrape tweets including quoted tweets from choosen accounts that have atleast 20 replies
    threads_df = scrapper.threads(accounts, tweets_df) #scrape threads. the tweets which the account replied to their main tweet
    replies_df = scrapper.replies(accounts, tweets_df) #scrape replies. replies that have atleast 5 likes
    replies_df = scrapper.rm_dup(threads_df['Thread'], replies_df) #remove thread tweets from replies
    all_tweets = scrapper.merge_dfs(tweets_df, threads_df, replies_df) #merge all tweets, threads and replies dataframe using common tweet Id
    all_tweets = scrapper.preprocess(all_tweets) #clean texts in threads and replies
    tweets_and_sentiments = sentiment.do(all_tweets) #sentiment analysis on cleaned threads and replies
    api.initial(tweets_and_sentiments) #initialize REST API with 6 endpoints


