#! /usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------------
"""
Author: Shayan Hodai shayan.hodai@gmail.com
Date: 4 March 2023
Purpose: Scrape tweets from choosen accounts, do sentiment analysis on threads and replies, create and update database on mongodb cloud, retrieve database and build REST API with 6 endpoints
"""
import argparse
import scrapper
import sentiment
import db
import api
# ----------------------------------------------------------------------------------------------------------------------


def get_args():
    """
    function to get arguments from command line
    input: None
    output: command line arguments
    """
    parser = argparse.ArgumentParser(description="description: scrape tweets from choosen accounts, do sentiment analysis on threads and replies, create and update database on mongodb cloud, retrieve database and build REST API with 6 endpoints")
    parser.add_argument("-a", "--account", default=["elonmusk", "ylecun", "BarackObama"], metavar="chosen twitter account(s)", nargs="+")

    return parser.parse_args()
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    args = get_args()
    accounts = args.account
    tweets_df = scrapper.tweets(accounts)  # scrape tweets including quoted tweets from choosen accounts that have atleast 20 replies
    threads_df = scrapper.threads(accounts, tweets_df)  # scrape threads. the tweets which the account replied to their main tweet
    replies_df = scrapper.replies(accounts, tweets_df)  # scrape replies. replies that have atleast 5 likes
    replies_df = scrapper.rm_dup(threads_df["Thread"], replies_df)  # remove thread tweets from replies
    all_tweets = scrapper.merge_dfs(tweets_df, threads_df, replies_df)  # merge all tweets, threads and replies dataframe using common tweet Id
    all_tweets = scrapper.preprocess(all_tweets)  # clean texts in threads and replies
    tweets_and_sentiments = sentiment.do(all_tweets) # sentiment analysis on cleaned threads and replies
    db.update(tweets_and_sentiments)  # update the database on mongodb cloud
    api.retrieve_db()  # retrieve database from mongodb cloud
    api.initial()  # initialize flask