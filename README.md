# twitter-analysis
The repository contains code to scrape tweets from the list of choosen accounts using snscrape module and do sentiment analysis, using hugging face's bert transformer, on threads and replies, create and update the database on mongodb cloud and build a REST API with 6 endpoints using flask


1. clone the repository to your local machine:
git clone https://github.com/ShayanHodai/twitter-analysis.git
2. run ./env.sh # it creates a virtual environemt and install required packages for ubuntu 20.04
3. activate the virtual environment:
source [the directory you cloned the repo]/venv/twitter/bin/activate
##### program is connected to my database, in order to create a new database and connect to yours do the followings:
4. create a cluster on  mongodb cloud, https://cloud.mongodb.com
5. connect/connect your application chose python driver and version 3.6 or later and copy the provided code, replace your password 
6. replace the code you copied with value of conn_str variable in db.py and api.py files
##### 7. run ./main.py --account twitter account # defaults accounts are ["elonmusk", "ylecun", "BarackObama"]
-----------------------------------------------------------------------------------------------------------------------------------------------------------
Done! depends on the number of tweets the program takes time to run, when the program finishes you created a database and built an API with 6 endpoints which you have access from your local machine.

http://127.0.0.1:5000/accounts -> returns json file of the accounts

http://127.0.0.1:5000/threads/account-handle -> returns json file of the threads

http://127.0.0.1:5000/replies/account-handle -> returns json file of the replies

http://127.0.0.1:5000/audience/account-handle -> returns json file of the audince (the accounts who replied to the tweet)

http://127.0.0.1:5000/threads_sentiment/account-handle -> returns json file of the threads sentiment

http://127.0.0.1:5000/replies_sentiment/account-handle -> returns json file of the replies sentiment
