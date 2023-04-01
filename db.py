"""
this module create and update database on mangodb cloud
"""
import pymongo
from bson import ObjectId
# ----------------------------------------------------------------------------------------------------------------------


def update(tweets_and_sentiments):
    """
    function to create and update databases on mongodb
    input: dataframe, all_tweets
    output: None, it updates the databases on mongodb cloud
    """
    conn_str = 'mongodb+srv://shayanhodai:<password>@cluster0.kfe3wix.mongodb.net/?retryWrites=true&w=majority'

    try:
        client = pymongo.MongoClient(conn_str)  # connect to mongo db
    except Exception:
        print('Error:{0}'.format(Exception))
    else:
        twitter_db = client['twitter_db']  # create accounts database

    # create collections in the database
    accounts_col = twitter_db['accounts']
    threads_col = twitter_db['threads']
    replies_col = twitter_db['replies']
    audience_col = twitter_db['audience']
    threads_sentiment_col = twitter_db['threads_sentiment']
    replies_sentiment_col = twitter_db['replies_sentiment']

    # delete all previous data in the records
    accounts_col.delete_many({})
    threads_col.delete_many({})
    replies_col.delete_many({})
    audience_col.delete_many({})
    threads_sentiment_col.delete_many({})
    replies_sentiment_col.delete_many({})

    num_rows = len(tweets_and_sentiments.index)
    mongoid = [str(ObjectId()) for i in range(num_rows)]

    # add newly gathered data in the records
    accounts = [{ '_id': str(ObjectId()), 'accounts': tweets_and_sentiments['Account'].unique().tolist()}] # accounts data
    accounts_col.insert_many(accounts)

    threads = []  # threads data
    for each_row in range(num_rows):
        instance = {}
        instance['_id'] = mongoid[each_row]
        instance['id'] = tweets_and_sentiments.loc[each_row, 'Id']
        instance['date'] = tweets_and_sentiments.loc[each_row, 'Date']
        instance['account'] = tweets_and_sentiments.loc[each_row, 'Account']
        instance['threads'] = tweets_and_sentiments.loc[each_row, 'Thread']
        threads.append(instance)
    threads_col.insert_many(threads)

    replies = []  # replies data
    for each_row in range(num_rows):
        instance = {}
        instance['_id'] = mongoid[each_row]
        instance['id'] = tweets_and_sentiments.loc[each_row, 'Id']
        instance['date'] = tweets_and_sentiments.loc[each_row, 'Date']
        instance['account'] = tweets_and_sentiments.loc[each_row, 'Account']
        instance['replies'] = tweets_and_sentiments.loc[each_row, 'Reply']
        replies.append(instance)
    replies_col.insert_many(replies)

    audience = []  # audience data
    for each_row in range(num_rows):
        instance = {}
        instance['_id'] = mongoid[each_row]
        instance['id'] = tweets_and_sentiments.loc[each_row, 'Id']
        instance['date'] = tweets_and_sentiments.loc[each_row, 'Date']
        instance['account'] = tweets_and_sentiments.loc[each_row, 'Account']
        instance['audience'] = tweets_and_sentiments.loc[each_row, 'Audience']
        audience.append(instance)
    audience_col.insert_many(audience)

    threads_sentiment = []  # threads_sentiment data
    for each_row in range(num_rows):
        instance = {}
        instance['_id'] = mongoid[each_row]
        instance['id'] = tweets_and_sentiments.loc[each_row, 'Id']
        instance['date'] = tweets_and_sentiments.loc[each_row, 'Date']
        instance['account'] = tweets_and_sentiments.loc[each_row, 'Account']
        instance['threads_sentiment'] = tweets_and_sentiments.loc[each_row, 'Thread_Sentiment']
        threads_sentiment.append(instance)
    threads_sentiment_col.insert_many(threads_sentiment)

    replies_sentiment = []  # replies_sentiment data
    for each_row in range(num_rows):
        instance = {}
        instance['_id'] = mongoid[each_row]
        instance['id'] = tweets_and_sentiments.loc[each_row, 'Id']
        instance['date'] = tweets_and_sentiments.loc[each_row, 'Date']
        instance['account'] = tweets_and_sentiments.loc[each_row, 'Account']
        instance['replies_sentiment'] = tweets_and_sentiments.loc[each_row, 'Reply_Sentiment']
        replies_sentiment.append(instance)
    replies_sentiment_col.insert_many(replies_sentiment)

    return None
