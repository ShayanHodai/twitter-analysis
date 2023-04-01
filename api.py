"""
this module build API with 6 endpoints using flask to serve requests
"""
from flask import Flask, Response
import pymongo
import psutil
import json
app = Flask(__name__)
# ----------------------------------------------------------------------------------------------------------------------


def retrieve_db():
    """
    function to retrieve database from mongodb cloud
    input: None
    output: None
    """
    conn_str = 'mongodb+srv://shayanhodai:rHxoSOBuvoNF0Bt2@cluster0.kfe3wix.mongodb.net/?retryWrites=true&w=majority'
    client = pymongo.MongoClient(conn_str)
    global twitter_db
    twitter_db = client.twitter_db
    # store documents in collections as a JSON file
    with open('accounts_json', 'w') as outfile:
        json.dump(list(twitter_db.accounts.find({})), outfile)
    with open('threads_json', 'w') as outfile:
        json.dump(list(twitter_db.threads.find({})), outfile)
    with open('replies_json', 'w') as outfile:
        json.dump(list(twitter_db.replies.find({})), outfile)
    with open('audience_json', 'w') as outfile:
        json.dump(list(twitter_db.audience.find({})), outfile)
    with open('threads_sentiment_json', 'w') as outfile:
        json.dump(list(twitter_db.threads_sentiment.find({})), outfile)
    with open('replies_sentiment_json', 'w') as outfile:
        json.dump(list(twitter_db.replies_sentiment.find({})), outfile)

    return None
# ----------------------------------------------------------------------------------------------------------------------


def initial():
    """
    function to initialize flask
    input: None
    output: None
    """
    used_ports = []
    for conn in psutil.net_connections():
        if conn.status == 'LISTEN':
            used_ports.append(conn.laddr.port)
    if not 5000 in used_ports:
        app.run(host='0.0.0.0', port=5000)
    else:
        print('Running on http://127.0.0.1:5000')
        pass

    return None
# ----------------------------------------------------------------------------------------------------------------------


@app.route('/accounts')  # create accounts endpoint
def get_accounts():
    """get accounts data when a user goes to the related endpoint"""
    with open('accounts_json') as f:
        json_data = json.load(f)
    response = Response(json.dumps(json_data, indent=2), mimetype='application/json')

    return response
# ----------------------------------------------------------------------------------------------------------------------


@app.route('/threads')  # create threads endpoint
@app.route('/threads/<account>')  # create threads endpoint with account handler
def get_threads(account=None):
    """get threads data when a user goes to the related endpoint"""
    with open('threads_json') as f:
        json_data = json.load(f)
    if account:  # if an account is chosen, filter that account data
        filtered_data = [item for item in json_data if item['account'] == account]
    else:  # else, data from all accounts
        filtered_data = json_data
    response = Response(json.dumps(filtered_data, indent=2), mimetype='application/json')

    return response
# ----------------------------------------------------------------------------------------------------------------------


@app.route('/replies')  # create replies endpoint
@app.route('/replies/<account>')  # create replies endpoint with account handler
def get_replies(account=None):
    """get replies data when a user goes to the related endpoint"""
    with open('replies_json') as f:
        json_data = json.load(f)
    if account:  # if an account is chosen, filter that account data
        filtered_data = [item for item in json_data if item['account'] == account]
    else:  # else, data from all accounts
        filtered_data = json_data
    response = Response(json.dumps(filtered_data, indent=2), mimetype='application/json')

    return response
# ----------------------------------------------------------------------------------------------------------------------


@app.route('/audience')  # create audience endpoint
@app.route('/audience/<account>')  # create audience endpoint with account handler
def get_audience(account=None):
    """get audience data when a user goes to the related endpoint"""
    with open('audience_json') as f:
        json_data = json.load(f)
    if account:  # if an account is chosen, filter that account data
        filtered_data = [item for item in json_data if item['account'] == account]
    else:  # else, data from all accounts
        filtered_data = json_data
    response = Response(json.dumps(filtered_data, indent=2), mimetype='application/json')

    return response
# ----------------------------------------------------------------------------------------------------------------------


@app.route('/threads_sentiment')  # create threads_sentiment endpoint
@app.route('/threads_sentiment/<account>')  # create threads_sentiment endpoint with account handler
def get_threads_sentiment(account=None):
    """get threads_sentiment data when a user goes to the related endpoint"""
    with open('threads_sentiment_json') as f:
        json_data = json.load(f)
    if account:  # if an account was chosen, filter that account data
        filtered_data = [item for item in json_data if item['account'] == account]
    else:  # else, data from all accounts
        filtered_data = json_data
    response = Response(json.dumps(filtered_data, indent=2), mimetype='application/json')
    
    return response

# ----------------------------------------------------------------------------------------------------------------------


@app.route('/replies_sentiment')  # create replies_sentiment endpoint
@app.route('/replies_sentiment/<account>')  # create replies_sentiment endpoint with account handler
def get_replies_sentiment(account=None):
    """get replies_sentiment data when a user goes to the related endpoint"""
    with open('replies_sentiment_json') as f:
        json_data = json.load(f)
    if account:  # if an account was chosen, filter that account data
        filtered_data = [item for item in json_data if item['account'] == account]
    else:  # else, data from all accounts
        filtered_data = json_data
    response = Response(json.dumps(filtered_data, indent=2), mimetype='application/json')
    
    return response