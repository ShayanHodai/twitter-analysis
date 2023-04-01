#! /bin/bash

python3 -m venv $(pwd)/venv/twitter
source $(pwd)/venv/twitter/bin/activate
pip install --upgrade pip
pip install snscrape
pip install tensorflow-cpu
pip install pandas
pip install Flask
pip install pymongo
pip install emoji==0.6.0
pip install psutil
pip install transformers
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
echo 
echo
echo 'Done! as of 2023-04-01 lastest version of required packages are installed succesfully.'
