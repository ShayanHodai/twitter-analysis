from transformers import pipeline
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def do(all_tweets):
    '''
    function to initialize sentiment analysis on threads and replies
    input: all tweets dataframe
    output: tweets_and_sentiments dataframe
    '''
    thread_sentiment = text_sentiment(all_tweets['Thread']) #threads sentiment analysis
    reply_sentiment = text_sentiment(all_tweets['Reply']) #replies sentiment analysis
    all_tweets['Thread_Sentiment'] = thread_sentiment
    all_tweets['Reply_Sentiment'] = reply_sentiment

    tweets_and_sentiments = all_tweets #rename the dataframe once it has sentiments

    return tweets_and_sentiments
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def text_sentiment(series_texts):
    '''
    function that goes through each reply in replies and each tweet in threads and do a sentiment analysis on all of them
    input: a column of either threads or replies
    output: a list which has many dictionaries inside and each of the dictionaries has a value of {'NEG':0 to 1, 'NEU': 0 to 1, 'POS': 0 to 1} showing how negative, neutral or positive each tweet is
    '''
    list_sentiment = []
    for texts in series_texts:
        d = {'NEG': 0, 'NEU': 0, 'POS': 0}
        for each_text in texts:
            sentiment = (bert_huggingface(each_text))
            d[sentiment[0]['label']] += sentiment[0]['score']
        for key in d: #calculate mean of sentiment score
            d[key] = '%.2f'%(d[key] / len(texts))
        list_sentiment.append(d)

    return list_sentiment
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def bert_huggingface(text):
    '''
    hugging face pre trained model called bert specifically trained to do sentiment analysis on tweets
    input: a tweet, string
    output: a list that contains a dictionary. the dictionary has 2 keys, label key would be negative, neutral or positive and the score key would be a floating point number between 0 to 1
    '''
    specific_model = pipeline('sentiment-analysis', model="finiteautomata/bertweet-base-sentiment-analysis", truncation=True)  #truncate the input sequence to the maximum length allowed by the model which is 128 for this model

    return specific_model(text)



