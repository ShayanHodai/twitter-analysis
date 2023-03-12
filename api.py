from flask import Flask, jsonify, request, Response
import psutil
import json
import time
import pandas as pd
app = Flask(__name__)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def release_port5000():
    '''
    first release port 5000, otherwise since the program runs automatically and port 5000 is already being used with the first run, the endpoints won't update
    input: None
    output: None
    '''
    pids = []
    for process in psutil.process_iter(): #find the process id of the main.py program which is running on 5000 port
        for arg in process.cmdline():
            if 'main.py' in arg:
                pids.append(process.pid)
    if len(pids) > 1: #if more than one process otherwise the the first running of the program going to be terminated
            terminate_process = psutil.Process(pids[0])
            terminate_process.terminate()

    time.sleep(10) #wait 10 seconds to release the port

    return None
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def initial(tweets_and_sentiments):
    '''
    function to initialize and build REST API with 6 endpoints to serve requests
    input: tweets_and_sentiments dataframe
    output: None. it just build the REST API with 6 endpoints
    '''
    num_rows = len(tweets_and_sentiments.index)

    accounts = [{'accounts': tweets_and_sentiments['Account'].unique().tolist()}]
    with open('accounts_json', 'w') as outfile:  #write accounts to a JSON file
        json.dump(accounts, outfile)

    threads = []
    for each_row in range(num_rows):
        instance = {}
        instance['id'] = tweets_and_sentiments.loc[each_row, 'Id']
        instance['date'] = tweets_and_sentiments.loc[each_row, 'Date']
        instance['account'] = tweets_and_sentiments.loc[each_row, 'Account']
        instance['threads'] = tweets_and_sentiments.loc[each_row, 'Thread']
        threads.append(instance)
    with open('threads_json', 'w') as outfile:  #write threads to a JSON file
        json.dump(threads, outfile)

    replies = []
    for each_row in range(num_rows):
        instance = {}
        instance['id'] = tweets_and_sentiments.loc[each_row, 'Id']
        instance['date'] = tweets_and_sentiments.loc[each_row, 'Date']
        instance['account'] = tweets_and_sentiments.loc[each_row, 'Account']
        instance['replies'] = tweets_and_sentiments.loc[each_row, 'Reply']
        replies.append(instance)
    with open('replies_json', 'w') as outfile:  #write replies to a JSON file
        json.dump(replies, outfile)

    audience = []
    for each_row in range(num_rows):
        instance = {}
        instance['id'] = tweets_and_sentiments.loc[each_row, 'Id']
        instance['date'] = tweets_and_sentiments.loc[each_row, 'Date']
        instance['account'] = tweets_and_sentiments.loc[each_row, 'Account']
        instance['audience'] = tweets_and_sentiments.loc[each_row, 'Audience']
        audience.append(instance)
    with open('audience_json', 'w') as outfile:  #write audience to a JSON file
        json.dump(audience, outfile)

    threads_sentiment = []
    for each_row in range(num_rows):
        instance = {}
        instance['id'] = tweets_and_sentiments.loc[each_row, 'Id']
        instance['date'] = tweets_and_sentiments.loc[each_row, 'Date']
        instance['account'] = tweets_and_sentiments.loc[each_row, 'Account']
        instance['threads_sentiment'] = tweets_and_sentiments.loc[each_row, 'Thread_Sentiment']
        threads_sentiment.append(instance)
    with open('threads_sentiment_json', 'w') as outfile:  #write threads_sentiment to a JSON file
        json.dump(threads_sentiment, outfile)

    replies_sentiment = []
    for each_row in range(num_rows):
        instance = {}
        instance['id'] = tweets_and_sentiments.loc[each_row, 'Id']
        instance['date'] = tweets_and_sentiments.loc[each_row, 'Date']
        instance['account'] = tweets_and_sentiments.loc[each_row, 'Account']
        instance['replies_sentiment'] = tweets_and_sentiments.loc[each_row, 'Reply_Sentiment']
        replies_sentiment.append(instance)
    with open('replies_sentiment_json', 'w') as outfile:  #write replies_sentiment to a JSON file
        json.dump(replies_sentiment, outfile)

    #release_port5000()

    app.run(host='0.0.0.0', port=5000) #enable access to the endpoints since it is running on a virtual machine on a cloud server

    return None
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/accounts') #create accounts endpoint
def get_accounts():
    with open('accounts_json') as f:
        json_data = json.load(f)
    response = Response(json.dumps(json_data, indent=2), mimetype='application/json')
    return response
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/threads') #create threads endpoint
def get_threads():
    with open('threads_json') as f:
        json_data = json.load(f)
    response = Response(json.dumps(json_data, indent=2), mimetype='application/json')
    return response
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/replies') #create replies endpoint
def get_replies():
    with open('replies_json') as f:
        json_data = json.load(f)
    response = Response(json.dumps(json_data, indent=2), mimetype='application/json')
    return response
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/audience') #create audience endpoint
def get_audience():
    with open('audience_json') as f:
        json_data = json.load(f)
    response = Response(json.dumps(json_data, indent=2), mimetype='application/json')
    return response
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/threads_sentiment') #create threads_sentiment endpoint
def get_threads_sentiment():
    with open('threads_sentiment_json') as f:
        json_data = json.load(f)
    response = Response(json.dumps(json_data, indent=2), mimetype='application/json')
    return response

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/replies_sentiment') #create replies_sentiment endpoint
def get_replies_sentiment():
    with open('replies_sentiment_json') as f:
        json_data = json.load(f)
    response = Response(json.dumps(json_data, indent=2), mimetype='application/json')
    return response
