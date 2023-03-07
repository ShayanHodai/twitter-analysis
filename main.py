#! /usr/bin/env python
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import scrapper
#import gpt

accounts = ['ylecun', 'alikarimi_ak8', 'elonmusk'] #accounts which we want to scrape tweets from

if __name__ == '__main__':
    tweets_df = scrapper.tweets(accounts)
    threads_df = scrapper.threads(accounts, tweets_df)
    replies_df = scrapper.replies(accounts, tweets_df)
    replies_df = scrapper.rm_dup(threads_df['Thread'], replies_df)
    all_tweets = scrapper.merge_dfs(tweets_df, threads_df, replies_df)
    all_tweets = scrapper.preprocess(all_tweets)
    print(all_tweets.head())
    #sentiment_threads = gpt.sentiment_threads(cleaned_tweets['Threads'])
    #sentiment_replies = gpt.sentiment_replies(cleaned_tweets['Replies'])
    #active users
