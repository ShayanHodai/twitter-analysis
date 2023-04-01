"""
this module scrape tweets from chosen accounts
"""
import snscrape.modules.twitter as sntwitter
import numpy as np
import pandas as pd
import emoji
import re
import warnings
warnings.filterwarnings("ignore")
# ----------------------------------------------------------------------------------------------------------------------


def tweets(accounts):
    """"
    function to scrape tweets from accounts
    input: list of accounts
    output: tweets dataframe containing tweets from each account
    """
    tweets = []
    for account in accounts:
        for limit, tweet in enumerate(sntwitter.TwitterSearchScraper('from:{0} since:2023-2-01 min_replies:20 -filter:replies'.format(account)).get_items()):  # scrape tweets and quote tweets since the given date which are not replies to other tweets and have at least 20 replies
            if limit >= 500:  # maximum number of tweets. 500 tweets from each account
                break
            tweets.append([tweet.id, tweet.date, tweet.username, tweet.content])  # the features we want from tweets

    tweets_df = pd.DataFrame(tweets, columns=['Id', 'Date', 'Username', 'Tweet']) # creating tweets dataframe

    return tweets_df
# ----------------------------------------------------------------------------------------------------------------------


def threads(accounts, tweets_df):
    """
    function to scrape threads from accounts
    inputs: list of accounts, tweets dataframe
    output: threads dataframe containing replies of the accounts to their first tweet
    """
    threads = []
    for id in tweets_df['Id']:
        for limit, thread in enumerate(sntwitter.TwitterSearchScraper('to:{0} AND from:{0} AND conversation_id:{1}'.format(tweets_df[tweets_df['Id'] == id]['Username'].values[0],id)).get_items()):  # scrape threads to tweets
            if limit >= 25:  # maximum number of thread tweets
                break
            threads.append([id, thread.content])  # the features we want from threads

    df = pd.DataFrame(threads, columns=['Id', 'Thread'])  # creating a dataframe

    array_threads = [] # threads be a list of arrays which each array contains all threads to the tweet
    for id in df['Id'].unique():
        array_threads.append(df[df['Id'] == id]['Thread'].values)

    threads_df = pd.DataFrame(columns=('Id', 'Thread')) # creating threads dataframe
    threads_df['Id'] = df['Id'].unique()
    threads_df['Thread'] = array_threads

    return threads_df
# ----------------------------------------------------------------------------------------------------------------------


def replies(accounts, tweets_df):
    """
    function to scrape replies
    inputs: list of accounts, tweets dataframe
    output: replies dataframe
    """
    replies = []
    for id in tweets_df['Id']:
        for limit, reply in enumerate(sntwitter.TwitterSearchScraper('to:{0} OR from:{0} conversation_id:{1} AND min_faves:5'.format(tweets_df[tweets_df['Id'] == id]['Username'].values[0],id)).get_items()):  # scrape replies to tweets which have at least 5 likes
            if limit >= 200:  # maximum number of replies. 200 replies to each tweet
                break
            replies.append([id, reply.username, reply.content])  # the features we want from replies

    df = pd.DataFrame(replies, columns=['Id', 'Username', 'Reply']) # creating a dataframe

    array_replies = [] # replies be a list of arrays which each array contains all replies to the tweet
    replied_users = []
    for id in df['Id'].unique():
        array_replies.append(df[df['Id'] == id]['Reply'].values)
        replied_users.append(list(df[df['Id'] == id]['Username'].values))

    replies_df = pd.DataFrame(columns=('Id', 'Replied_User', 'Reply')) # creating replies dataframe
    replies_df['Id'] = df['Id'].unique()
    replies_df['Replied_User'] = replied_users
    replies_df['Reply'] = array_replies

    return replies_df
# ----------------------------------------------------------------------------------------------------------------------


def rm_dup(threads, replies_df):
    """
    thread tweets are in both replies dataframe and threads dataframe. drop these rows from replies dataframe
    inputs: threads column, replies dataframe
    output: dataframe without duplicate rows
    """
    dup_ind = []
    for thread in threads:
        if thread in replies_df['Reply'].values:
            dup_ind.append(replies_df[replies_df['Reply'] == thread].index[0])

    return replies_df.drop(index=dup_ind).reset_index(drop=True)
# ----------------------------------------------------------------------------------------------------------------------


def merge_dfs(tweets_df, threads_df, replies_df):
     """
     merge all tweets, threads and replies dataframe using common Id and create a new data frame containing all data
     inputs: tweets dataframe, threads dataframe, replies dataframe
     output: all_tweets dataframe containing all data
     """
     noreply = [] # first remove tweets which don't have any reply with more than 5 likes
     for id in tweets_df['Id']:
         if id not in replies_df['Id'].values:
             noreply.append(tweets_df[tweets_df['Id'] == id].index.values[0])

     tweets_df = tweets_df.drop(index=noreply).reset_index(drop=True)

     tweets_replies = pd.merge(tweets_df, replies_df, on='Id') # merge tweets_df and replies_df using common Id

     array_thread = [] # now merge threads_df with tweets_df and replies_df. it is very important to keep in mind that threads are tweets which the account we are interested in replied to the their own first tweets
     for id in tweets_df['Id']:
         if id in threads_df['Id'].values:
             new_list = [] # if the tweet has threads, gather all threads into a list
             new_list.append(tweets_df[tweets_df['Id'] == id]['Tweet'].values[0]) # append the first tweet
             for i in threads_df[threads_df['Id'] == id]['Thread']: # first get the threads of the tweet
                 for each_thread in i: # then go through each thread
                     new_list.append(each_thread) # add each of the thread to the new list along side the first tweet
             array_thread.append(np.array(new_list, dtype=object)) # once we gather the first tweet and all of threads append them all to the list
         else:
             array_thread.append(tweets_df[tweets_df['Id'] == id]['Tweet'].values) # if the first tweets doesn't have any thread

     tweets_replies['Tweet'] = array_thread
     all_tweets = tweets_replies.rename(columns={'Tweet': 'Thread'}) # rename tweet column to thread because now it has threads not only the first tweet. the dataframe has finally all related tweets together

     return all_tweets
# ----------------------------------------------------------------------------------------------------------------------


def preprocess(all_tweets):
    """
    preprocess dataframe. clean texts in threads and replies
    input: all_tweets dataframe
    output: cleaned all_tweets dataframe
    """
    for ind, username in enumerate(all_tweets['Username']): # we don't want to the user itself to be considered as an active user who is replying to its tweet. other users who are interacting are active users. so we remove the user from the list of users who replied
        for replied_user in all_tweets.loc[ind, 'Replied_User'][:]:
            if replied_user == username:
                all_tweets.loc[ind, 'Replied_User'].remove(username)

    clean_thread = [] # cleaning each thread
    for all_thread in all_tweets['Thread']:
        new_list = []
        for each_thread in all_thread:
            new_list.append(clean_text(each_thread))
        clean_thread.append(new_list)

    clean_reply = [] # cleaning rach reply
    for all_reply in all_tweets['Reply']:
        new_list = []
        for each_reply in all_reply:
            new_list.append(clean_text(each_reply))
        clean_reply.append(new_list)

    all_tweets['Thread'] = clean_thread
    all_tweets['Reply'] = clean_reply


    for all_thread in all_tweets['Thread']: # there are some tweets that only contain a meme or a mention since we have remove any url and mention from tweets, now they have white spaces as input. remove them from the threads
        for each_thread in all_thread[:]:
            if each_thread == ' ':
                all_thread.remove(' ')
            elif each_thread == '':
                all_thread.remove('')
            elif each_thread == [' ']:
                all_thread.remove([' '])

    empty_threads = [] # now that we removed white spaces from list of threads there might be some threads that become empty, []. drop these rows
    for ind, all_thread in enumerate(all_tweets['Thread']):
        if not all_thread:
            empty_threads.append(ind)

    all_tweets = all_tweets.drop(index=empty_threads).reset_index(drop=True)

    for all_reply in all_tweets['Reply']:  # there are multiple replies that only contain a meme or a mention since we have remove any url and mention from tweets, now they have white spaces as input. remove them from the threa
        for each_reply in all_reply[:]:
            if each_reply == ' ':
                all_reply.remove(' ')
            elif each_reply == '':
                all_reply.remove('')
            elif each_reply == [' ']:
                all_reply.remove([' '])

    all_tweets = all_tweets.rename(columns={'Username': 'Account'})  # rename username column to account
    all_tweets = all_tweets.rename(columns={'Replied_User': 'Audience'})  # rename replied_user column to audience
    all_tweets['Date'] = all_tweets['Date'].astype(str)  # convert dtype of date column to str because timestamp is not JSON serializable which we need to be for building the API
    all_tweets['Id'] = all_tweets['Id'].astype(str)  # convert dtype of id column to str because int64 is not JSON serializable which we need to be for building the API

    return all_tweets
# ----------------------------------------------------------------------------------------------------------------------


def clean_text(text):
    """
    function to remove any unwanted character from the text and convert some shortened form to the full form
    input: text
    output: cleaned text
    """
    text = text.lower()
    text = ''.join(char for char in text if char in emoji.UNICODE_EMOJI or ord(char) < 128) # remove any non ascii characters except emojis
    text = re.sub(r'\n', ' ', text)  # remove \n new line
    text = re.sub(r'@([A-Za-z0-9_]+)', '', text)  # remove @mentions
    text = re.sub(r'http\S+|https\S+', ' ', text)  # remove http and https links
    text = re.sub('n\'t', ' not', text)
    text = re.sub('\'', '', text)
    text = re.sub('\s+', ' ', text)  # converts any more than one space to one space

    return text
