# twitter-analysis
The repository contains code to scrape tweets from the list of choosen accounts using snscrape module and do sentiment analysis, using hugging face's bert transformer, on threads and replies, create and update the database on mongodb cloud and build a REST API with 6 endpoints using flask


1. clone the repository to your local machine:
git clone https://github.com/ShayanHodai/twitter-analysis.git
2. create a virtual environment inside the directory where you cloned the codes:
python3 -m venv [the directory you cloned the repo]/venv/twitter
3. activate the virtual environment:
source [the directory you cloned the repo]/venv/twitter/bin/activate
4. upgrade pip:
pip install --upgrade pip
5. install required modules: 
pip install -r requirements.txt # packages are for ubuntu 20.04
# program is connected to my database, in order to create a new database and connect to yours do the followings:
6. create a cluster on  mongodb cloud, https://cloud.mongodb.com
7. from <connect> select <connect your application> chose python driver and version 3.6 or later and copy the provided code, replace your password  with <password>
8. replace the code you copied with value of conn_str variable in db.py and api.py files
9. run ./main.py 
-----------------------------------------------------------------------------------------------------------------------------------------------------------
Done! depends on the number of tweets the program takes time to run
when the program finishes you created a database and built an API with 6 endpoints which you have access from your local machine.

http://127.0.0.1:5000/accounts -> returns json file of the accounts

http://127.0.0.1:5000/threads/account-handle -> returns json file of the threads

http://127.0.0.1:5000/replies/account-handle -> returns json file of the replies

http://127.0.0.1:5000/audience/account-handle -> returns json file of the audince (the accounts who replied to the tweet)

http://127.0.0.1:5000/threads_sentiment/account-handle -> returns json file of the threads sentiment

http://127.0.0.1:5000/replies_sentiment/account-handle -> returns json file of the replies sentiment

OR either have access to the endpoints through my virtual machine running on a clouad server at http://20.81.153.226:5000/same endpoints as above
