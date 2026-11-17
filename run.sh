#!/bin/bash

# initialize and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install backend dependencies
pip install -r requirements.txt

# install frontend dependencies
npm install

# rebuild fresh copy of database
bash backend/build_db.sh

# run the application
npm run dev
