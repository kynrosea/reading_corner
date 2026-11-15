from flask import Blueprint, jsonify, request
from app.db import get_db, close_db
from app.util import build_sql_statement
from datetime import date
from app import config
import sqlite3

library_bp = Blueprint('library', __name__)

@library_bp.get('/<username>')
def get_user_library(username):
    if not username:
        return jsonify({'error' : 'Username is required'})
    
    conn = get_db()
    
    sql = (
        'SELECT * FROM user_books '
        'WHERE username=?'
    )

    books = conn.execute(sql, (username,)).fetchall()

    close_db()

    if not books:
        return jsonify({'message' : 'No books found in library'}), 200

    return jsonify([dict(b) for b in books]), 200

@library_bp.put('/<username>/<author>/<title>')
def update_library_book(username, author, title):
    if not username or not title or not author:
        return jsonify({'error' : 'Username, author, and title required'}), 400
    
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400
    
    data = request.get_json()

    if not data:
        return jsonify({'error' : 'JSON data is required'}), 400

    status = data.get('status') or None
    category = data.get('category') or None
    start_date = data.get('start_date') or None
    finished_date = data.get('finished_date') or None

    conn = get_db()

    errors = {}
    
    if status:
        sql = (
            'UPDATE user_library '
            'SET status=? '
            'WHERE (user_id, book_id) = ('
            '   SELECT user_id, book_id '
            '   FROM user_books '
            '   WHERE username=? AND title=? AND author=?)'
        )

        conn.execute(sql, (status, username, title, author))

        sql = (
            'SELECT status FROM user_library '
            'WHERE (user_id, book_id) = ('
            '   SELECT user_id, book_id '
            '   FROM user_books '
            '   WHERE username=? AND title=? AND author=?)'
        )

        row = conn.execute(sql, (username, title, author)).fetchone()
        
        if not row:
            return jsonify({'error' : 'record retrieval failed'}), 404

        if row['status'] != status:
            errors['status'] = 'status update failed'

    if category:
        sql = (
            'UPDATE user_library '
            'SET category=? '
            'WHERE (user_id, book_id) = ('
            '   SELECT user_id, book_id '
            '   FROM user_books '
            '   WHERE username=? AND title=? AND author=?)'
        )

        conn.execute(sql, (category, username, title, author))
        
        sql = (
            'SELECT category FROM user_library '
            'WHERE (user_id, book_id) = ('
            '   SELECT user_id, book_id '
            '   FROM user_books '
            '   WHERE username=? AND title=? AND author=?)'
        )

        row = conn.execute(sql, (username, title, author)).fetchone()
        if not row:
            return jsonify({'error' : 'record retrieval failed'}), 404

        if row['category'] != category:
            errors['category'] = 'category update failed'

    if start_date:
        sql = (
            'UPDATE user_library '
            'SET start_date=? '
            'WHERE (user_id, book_id) = ('
            '   SELECT user_id, book_id '
            '   FROM user_books '
            '   WHERE username=? AND title=? AND author=?)'
        )

        conn.execute(sql, (start_date, username, title, author))
        sql = (
            'SELECT start_date FROM user_library '
            'WHERE (user_id, book_id) = ('
            '   SELECT user_id, book_id '
            '   FROM user_books '
            '   WHERE username=? AND title=? AND author=?)'
        )

        row = conn.execute(sql, (username, title, author)).fetchone()
        if not row:
            return jsonify({'error' : 'record retrieval failed'}), 404
        
        if row['start_date'] != start_date:
            errors['start_date'] = 'start_date update failed'

    if finished_date:
        sql = (
            'UPDATE user_library '
            'SET finished_date=? '
            'WHERE (user_id, book_id) = ('
            '   SELECT user_id, book_id '
            '   FROM user_books '
            '   WHERE username=? AND title=? AND author=?)'
        )

        conn.execute(sql, (finished_date, username, title, author))
        
        sql = (
            'SELECT finished_date FROM user_library '
            'WHERE (user_id, book_id) = ('
            '   SELECT user_id, book_id '
            '   FROM user_books '
            '   WHERE username=? AND title=? AND author=?)'
        )

        row = conn.execute(sql, (username, title, author)).fetchone()
        if not row:
            return jsonify({'error' : 'record retrieval failed'}), 404

        if row['finished_date'] != finished_date:
            errors['finished_date'] = 'finished_date update failed'
    

    sql = (
        'SELECT * FROM user_library '
        'WHERE (user_id, book_id) = ('
        '   SELECT user_id, book_id '
        '   FROM user_books '
        '   WHERE username=? AND title=? AND author=?)'
    )

    update = conn.execute(sql, (username, title, author)).fetchone()

    close_db()
    
    if len(errors) > 0:
        return jsonify(e for e in errors), 404

    return jsonify(dict(update)), 200

@library_bp.post('/<username>/<author>/<title>')
def add_user_book(username, author, title):
    if not username or not author or not title:
        return jsonify({'error' : 'username, author, and title required'}), 400

    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    data = request.get_json()

    category = data.get('category') or None
    status = data.get('status')
    start_date = data.get('start_date') or None
    finished_date = data.get('finished_date') or None

    if not status:
        return jsonify({'error' : 'status is required'}), 400

    conn = get_db()

    sql = 'SELECT user_id FROM users WHERE username=?'

    row = conn.execute(sql, (username,)).fetchone()

    if not row:
        return jsonify({'error' : 'record retrieval failed'}), 404

    user_id = row['user_id']

    

    sql = 'SELECT book_id FROM books WHERE title=? AND author=?'
    row = conn.execute(sql, (title, author)).fetchone()
    
    if not row:
        return jsonify({'error' : 'record retrieval failed'}), 404

    book_id = row['book_id']

    sql, bindings = build_sql_statement(
            'user_library', 
            [user_id, book_id, status],
            ['user_id', 'book_id', 'status'],
            3,
            [category, start_date, finished_date],
            ['category', 'start_date', 'finished_date']
    )
        
    conn.execute(sql, tuple(bindings))

    sql = 'SELECT * FROM user_library WHERE user_id=? AND book_id=?'

    row = conn.execute(sql, (user_id, book_id)).fetchone()

    close_db()

    if not row:
        return jsonify({'error' : 'Insertion failed'}), 404

    return jsonify(dict(row)), 200

@library_bp.get('/<username>/query')
def filter_library(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    title = request.args.get('title')
    author = request.args.get('author')
    category = request.args.get('category')
    status = request.args.get('status')

    conn = get_db()
    results = {}

    if title:
        sql = (
            'SELECT * FROM user_library AS ul '
            'JOIN books AS b '
            '   ON ul.book_id = b.book_id '
            'JOIN users AS u '
            '   ON ul.user_id = u.user_id '
            'WHERE ('
            '   b.book_id IN (SELECT book_id FROM books WHERE title=?) '
            'AND '
            '   u.user_id = (SELECT user_id FROM users WHERE username=?) '
            ')'
        )

        sql = '''
            SELECT * FROM user_library AS ul
            JOIN books AS b
                ON ul.book_id = b.book_id
            JOIN users AS u
                ON ul.user_id = u.user_id
            WHERE
                b.book_id IN (SELECT book_id FROM books WHERE title=?)
                AND
                u.user_id = (SELECT user_id FROM users WHERE username=?)
        '''
        rows = conn.execute(sql, (title, username)).fetchall()

        if rows == []:
            return jsonify({'error' : 'record retrieval failed'}), 404
        
        for r in rows:
            user_id = r['user_id']
            book_id = r['book_id']
            results[(user_id, book_id)] = r
        
    if author:
        sql = '''
            SELECT * FROM user_library AS ul
            JOIN books AS b
                ON ul.book_id = b.book_id
            JOIN users AS u
                ON ul.user_id = u.user_id
            WHERE
                b.book_id IN (SELECT book_id FROM books WHERE author=?)
                AND
                u.user_id = (SELECT user_id FROM users WHERE username=?)
        '''

        rows = conn.execute(sql, (author, username)).fetchall()
        if rows == []:
            return jsonify({'error' : 'record retrieval failed'}), 404
        
        for r in rows:
            user_id = r['user_id']
            book_id = r['book_id']
            results[(user_id, book_id)] = r

    if category:
        sql = '''
            SELECT * FROM user_library AS ul
            JOIN users AS u
                ON ul.user_id = u.user_id
            WHERE ul.category=? AND u.username=?
        '''
        rows = conn.execute(sql, (category,username)).fetchall()
        if rows == []:
            return jsonify({'error' : 'record retrieval failed'}), 404
        
        for r in rows:
            user_id = r['user_id']
            book_id = r['book_id']
            results[(user_id, book_id)] = r

    if status:
        sql = '''
            SELECT * FROM user_library AS ul
            JOIN users AS u
                ON ul.user_id = u.user_id
            WHERE ul.status=? AND u.username=?
        '''
        rows = conn.execute(sql, (status, username)).fetchall()
        
        if rows == []:
            return jsonify({'error' : 'record retrieval failed'}), 404

        for r in rows:
            user_id = r['user_id']
            book_id = r['book_id']
            results[(user_id, book_id)] = r


    if len(results) == 0:
        return jsonify({'message' : 'Zero results matching query'}), 200

    return jsonify([dict(r) for r in results.values()]), 200

@library_bp.get('/logs/<username>')
def get_user_reading_logs(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    conn = get_db()

    sql = 'SELECT user_id FROM users WHERE username=?'
    user = conn.execute(sql, (username,)).fetchone()
    user_id = user['user_id']

    sql = '''
        SELECT * FROM reading_logs
        WHERE user_id=?
    '''

    rows = conn.execute(sql, (user_id,)).fetchall()

    close_db()
    
    if rows == []:
        return jsonify({'message' : 'user has no reading logs'}), 200

    return jsonify([dict(r) for r in rows]), 200

@library_bp.post('/logs/<username>')
def add_reading_log(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    if not request.is_json:
        return jsonify({'error' : 'Request must be a JSON object'}), 400

    log = request.get_json()

    if not log:
        return jsonify({'error' : 'JSON object data is required'}), 400

    book_id = log['book_id']
    log_date = date.today()
    progress = log['progress'] or None
    notes = log['notes'] or None
    session_time = log['session_time'] or None

    if not book_id:
        return jsonify({'error' : 'book_id is required'}), 400
    
    conn = get_db()


    sql = 'SELECT user_id FROM users WHERE username=?'
    row = conn.execute(sql, (username,)).fetchone()
    user_id = row['user_id']
    
    sql, bindings = build_sql_statement(
            'reading_logs',
            [user_id, book_id, log_date],
            ['user_id', 'book_id', 'log_date'],
            3,
            [progress, notes, session_time],
            ['progress', 'notes', 'session_time']
    )
    

    # automatically update book's read status if progress is 100 from log
    if progress == 100:
        try:
            conn.execute('BEGIN TRANSACTION')
            
            status_update = '''
                UPDATE user_library
                SET status="read"
                WHERE user_id=? AND book_id=?
            '''

            conn.execute(status_update, (user_id, book_id))
        
            cursor = conn.execute(sql, tuple(bindings))

            conn.execute('END TRANSACTION')

        except sqlite3.Error as e:
            conn.execute('ROLLBACK')
            return jsonify({'error' : e}), 404
        
        sql = 'SELECT * FROM reading_logs WHERE log_id=?'

        row = conn.execute(sql, (cursor.lastrowid,)).fetchone()
    else:

        cursor = conn.execute(sql, tuple(bindings))
        sql = 'SELECT * FROM reading_logs WHERE log_id=?'

        row = conn.execute(sql, (cursor.lastrowid,)).fetchone()


    close_db()

    if not row:
        return jsonify({'error' : 'log insertion failed'}), 404

    return jsonify(dict(row)), 200
    

        
