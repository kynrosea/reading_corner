#!/bin/bash


# install backend dependencies
pip install -r requirements.txt

# install frontend dependencies
npm --prefix frontend install

# rebuild fresh copy of database
bash backend/build_db.sh

# run the application
npm run dev
