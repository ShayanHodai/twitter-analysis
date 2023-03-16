# twitter-analysis
The repository contains code to scrape tweets from the list of choosen accounts using snscrape module and do sentiment analysis, using hugging face API, on threads and replies to each tweet and build a REST API with 6 endpoints 


1. clone the repository to your local machine:
git clone https://github.com/ShayanHodai/twitter-analysis.git
2. create a virtual environment inside the directory where you cloned the codes:
python3 -m venv [the directory you cloned the repo]/venv/twitter
3. activate the virtual environment:
source [the directory you cloned the repo]/venv/twitter/bin/activate
4. upgrade pip:
pip install --upgrade pip
5. install required modules: 
pip install -r requirements.txt #packages are for ubuntu 20.04
6. run ./main.py
-----------------------------------------------------------------------------------------------------------------------------------------------------------
Done! depends on the number of tweets the program takes time to run
when the program finishes you will have access to 6 endpoints from your local machine.
http://127.0.0.1:5000/accounts -> returns json file of the accounts
http://127.0.0.1:5000/threads/<account> -> returns json file of the threads
http://127.0.0.1:5000/replies/<account> -> returns json file of the replies
http://127.0.0.1:5000/audience/<account> -> returns json file of the audince (the accounts who replied to the tweet)
http://127.0.0.1:5000/threads_sentiment/<account> -> returns json file of the threads sentiment
http://127.0.0.1:5000/replies_sentiment/<account> -> returns json file of the replies sentiment

OR either have access to endpoints through my virtual machine running on a clouad server at http://20.81.153.226:5000/same endpoints as above
