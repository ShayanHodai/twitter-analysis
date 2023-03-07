#! /usr/bin/env python
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
import warnings
warnings.filterwarnings("ignore")
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def tweets(accounts):
    '''function to scrape tweets from each given accounts'''

    tweets = []
    for account in accounts:
        for limit, tweet in enumerate(sntwitter.TwitterSearchScraper('from:{0} since:2023-2-01 min_replies:20 -filter:replies'.format(account)).get_items()):  #scrape tweets and quote tweets since the given date which are not replies to other tweets and have at least 20 replies
            if limit >= 250:  #maximum number of tweets you want to scrape. 250 tweets from each account
                break
            tweets.append([tweet.id, tweet.date, tweet.username, tweet.content])  #the features we want from tweets

    tweets_df = pd.DataFrame(tweets, columns=['Id', 'Date', 'Username', 'Tweet']) #creating tweets dataframe
    return tweets_df
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def threads(accounts, tweets_df):
    '''function to scrape threads from each given accounts. the replies of each account to their initial tweet'''

    threads = []
    for id in tweets_df['Id']:
        for limit, thread in enumerate(sntwitter.TwitterSearchScraper('to:{0} AND from:{0} AND conversation_id:{1}'.format(tweets_df[tweets_df['Id'] == id]['Username'].values[0],id)).get_items()):  # scrape threads to scraped tweets
            if limit >= 25:  # maximum number of thread tweets
                break
            threads.append([id, thread.content])  #the features we want from threads

    df = pd.DataFrame(threads, columns=['Id', 'Thread'])  #creating a dataframe

    str_threads = [] #we want threads be a concatenated line of strings rather than separated series. all threads to a specific id must be assigned to that id
    for id in df['Id'].unique():
        str_threads.append(' '.join(df[df['Id'] == id]['Thread'].values))

    threads_df = pd.DataFrame(columns=('Id', 'Thread')) #creating threads dataframe
    threads_df['Id'] = df['Id'].unique()
    threads_df['Thread'] = str_threads

    return threads_df
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def replies(accounts, tweets_df):
    '''function to scrape replies to scraped tweets from each given accounts'''

    replies = []
    for id in tweets_df['Id']:
        for limit, reply in enumerate(sntwitter.TwitterSearchScraper('to:{0} OR from:{0} conversation_id:{1} AND min_faves:4'.format(tweets_df[tweets_df['Id'] == id]['Username'].values[0],id)).get_items()):  #scrape replies to scraped tweets which have at least 4 likes
            if limit >= 200:  #maximum number of replies. 200 replies to each tweet
                break
            replies.append([id, reply.username, reply.content])  #the features we want from replies

    df = pd.DataFrame(replies, columns=['Id', 'Username', 'Reply']) #creating a dataframe

    str_replies = [] #we want replies be a concatenated line of strings rather than separated series. all replies and users who replied to a specific id must be assigned to that id
    replied_users = []
    for id in df['Id'].unique():
        str_replies.append(' '.join(df[df['Id'] == id]['Reply'].values))
        replied_users.append(list(df[df['Id'] == id]['Username'].values))

    replies_df = pd.DataFrame(columns=('Id', 'Replied_User', 'Reply')) #creating replies dataframe
    replies_df['Id'] = df['Id'].unique()
    replies_df['Replied_User'] = replied_users
    replies_df['Reply'] = str_replies

    return replies_df
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def rm_dup(threads, replies_df):
    '''thread tweets are in both replies_df and threads_df. we need to drop these rows from replies_df'''

    dup_ind = []
    for thread in threads:
        if thread in replies_df['Reply'].values:
            dup_ind.append(replies_df[replies_df['Reply'] == thread].index[0])

    return replies_df.drop(index=dup_ind).reset_index(drop=True)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def merge_dfs(tweets_df, threads_df, replies_df):
     '''merge all tweets, threads and replies dataframe using common Id and create a new data frame containing all information'''
     noreply = [] #first we remove tweets which don't have any reply with more than 5 likes
     for id in tweets_df['Id']:
         if id not in replies_df['Id'].values:
             noreply.append(tweets_df[tweets_df['Id'] == id].index.values[0])

     tweets_df = tweets_df.drop(index=noreply).reset_index(drop=True)

     tweets_replies = pd.merge(tweets_df, replies_df, on='Id') #merge tweets_df and replies_df using common Id

     thread = [] #now merge threads_df with tweets_df and replies_df. very important to keep in mind that threads are tweets which the main account replied to the their first tweets
     for id in tweets_df['Id']:
         if id in threads_df['Id'].values:
             thread.append(''.join(tweets_df[tweets_df['Id'] == id]['Tweet'].values + ' ' + threads_df[threads_df['Id'] == id]['Thread'].values)) #if the first tweet has any thread
         else:
             thread.append(''.join(tweets_df[tweets_df['Id'] == id]['Tweet'].values)) #if the first tweets doesn't have thread

     tweets_replies['Tweet'] = thread
     all_tweets = tweets_replies.rename(columns={'Tweet': 'Thread'}) #rename tweet column to thread because now it has threads not only the first tweet. the dataframe has finally all related tweets together
     all_tweets= all_tweets.drop(columns='Id') #we need Ids anymore

     return all_tweets
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def preprocess(all_tweets):
    '''preprocess dataframe. clean texts in threads and replies '''
    for ind, username in enumerate(all_tweets['Username']): #we don't want to the user itself to be considered as an active user who is replying to the its tweet. we want other users who are interacting as active users. so we remove the user from the list of users who replied
        for replied_user in all_tweets.loc[0, 'Replied_User'][:]:
            if replied_user == username:
                all_tweets.loc[0, 'Replied_User'].remove(username)

    clean_thread = all_tweets['Thread'].apply(clean_text)
    clean_reply = all_tweets['Reply'].apply(clean_text)

    all_tweets['Thread'] = clean_thread
    all_tweets['Reply'] = clean_reply

    return all_tweets
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)  # remove \n new line
    text = re.sub(r'@([A-Za-z0-9_]+)', '', text)  # remove @mentions
    text = re.sub(r'http\S+|https\S+', '', text)  # remove http and https links
    text = re.sub(r'[^\w\s,?!]', '', text)  # remove emojis
    text = re.sub('n\'t', ' not', text)
    text = re.sub('\'s', ' is', text)
    text = re.sub('\'m', ' am', text)
    text = re.sub('\'ll', ' will', text)
    text = re.sub('\'re', ' are', text)
    text = re.sub('\'d', ' would', text)
    text = re.sub('\'', '', text)
    text = re.sub('\s+', ' ', text)  # converts any more than one space to one space
    return text