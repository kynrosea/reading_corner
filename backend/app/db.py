import sqlite3

from flask import g

# i will change this eventually
DB = 'reading_tracker.db'
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB, autocommit=True)
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    with open('app/sql/schema.sql', 'r', encoding='utf-8') as f:
        db.executescript(f.read())
    with open('app/sql/insert_data.sql', 'r', encoding='utf-8') as f:
        db.executescript(f.read())


