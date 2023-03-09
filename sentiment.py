from transformers import pipeline
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

def do(tweets_and_sentiments):
    thread_sentiment = text_sentiment(tweets_and_sentiments['Thread'])
    reply_sentiment = text_sentiment(tweets_and_sentiments['Reply'])
    tweets_and_sentiments['Thread_Sentiment'] = thread_sentiment
    tweets_and_sentiments['Reply_Sentiment'] = reply_sentiment
    return tweets_and_sentiments

def text_sentiment(series_texts):
    list_sentiment = []
    for texts in series_texts:
        d = {'NEG': 0, 'NEU': 0, 'POS': 0}
        for each_text in texts:
            sentiment = (bert_huggingface(each_text))
            d[sentiment[0]['label']] += sentiment[0]['score']
        for key in d:
            d[key] = d[key] / len(texts)

        list_sentiment.append(d)

def bert_huggingface(text):
    specific_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
    return specific_model(text)



