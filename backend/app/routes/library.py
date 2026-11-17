from flask import Blueprint, jsonify, request
from app.db import get_db, close_db
import sqlite3
from app.errors import ConflictError, NotFoundError

library_bp = Blueprint('library', __name__)

@library_bp.get('/<username>')
def get_user_library(username):
    if not username:
        return jsonify({'error' : 'Username is required'}), 400

    try:
        conn = get_db()
        
        sql = '''
            SELECT * 
            FROM user_books
            WHERE username=?
            ORDER BY author ASC
        '''

        books = conn.execute(sql, (username,)).fetchall()
        
        if books == []:
            return [], 200

        return jsonify([dict(b) for b in books]), 200

    except sqlite3.Error as e:
        return jsonify({'error' : str(e)})
            
    
@library_bp.put('/<username>/<title>/<author>')
def update_library_book(username, title, author):
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

    # try catch block to handle any random database errors
    try:

        conn = get_db()
        
        # ensuring user actually exists before performing updates
        sql = '''
            SELECT *
            FROM users
            WHERE username=?
        '''
        row = conn.execute(sql, (username,)).fetchone()

        if not row:
            raise NotFoundError('Could not find user')

        # ensuring book is actually in user's library
        sql = '''
            SELECT * 
            FROM user_library
            WHERE (user_id, book_id) = (
                SELECT user_id, book_id
                FROM user_books
                WHERE username=? AND title=? AND author=?
            )
        '''

        row = conn.execute(sql, (username, title, author)).fetchone()
        if not row:
            raise NotFoundError('Could not find book in your library')
        
        reward = None
        # treating the entire list of potential updates as transaction
        # if ANY update fails, then none of them will be saved
        # they must all succeed or fail together, especially the multiple steps in the status update

        conn.execute('BEGIN TRANSACTION');

        if status:

            sql = '''
                SELECT status 
                FROM user_library
                WHERE (user_id, book_id) = (
                    SELECT user_id, book_id
                    FROM user_books
                    WHERE username=? AND title=? AND author=?
                )
            '''

            row = conn.execute(sql, (username, title, author)).fetchone()
            current_status = row['status']
            
            # award 50 leaves to user for completing a book
            if current_status != 'read' and status == 'read':
                sql = '''
                    SELECT leaf_balance
                    FROM users 
                    WHERE username=?
                '''
                row = conn.execute(sql, (username,)).fetchone()

                former_leaf_balance = row['leaf_balance']
                
                sql = '''
                    UPDATE users
                    SET leaf_balance=leaf_balance+50
                    WHERE username=?
                '''

                conn.execute(sql, (username,))

                sql = '''
                    SELECT *
                    FROM users 
                    WHERE username=?
                '''

                row = conn.execute(sql, (username,)).fetchone()

                if not row:
                    raise sqlite3.Error('Could not retrieve record from users')
                
                if (row['leaf_balance']-50) != former_leaf_balance:
                    raise sqlite3.Error('Could not update leaf_balance')
                
                reward = {
                    'leaves_earned' : 50,
                    'message' : 'User earned 50 leaves'
                }

            
            sql = '''
                UPDATE user_library
                SET status=?
                WHERE (user_id, book_id) = (
                    SELECT user_id, book_id
                    FROM user_books
                    WHERE username=? AND title=? AND author=?
                )
            '''

            conn.execute(sql, (status, username, title, author))
            
            sql = '''
                SELECT status 
                FROM user_library
                WHERE (user_id, book_id) = (
                    SELECT user_id, book_id
                    FROM user_books
                    WHERE username=? AND title=? AND author=?
                )
            '''

            row = conn.execute(sql, (username, title, author)).fetchone()
            if not row:
                raise sqlite3.Error('Could not retrieve record from user_library')
            
            if row['status'] != status:
                raise sqlite3.Error('Could not update status')
            

            

        if category:
            
            sql = '''
                UPDATE user_library
                SET category=?
                WHERE (user_id, book_id) = (
                    SELECT user_id, book_id
                    FROM user_books
                    WHERE username=? AND title=? AND author=?
                )
            '''

            conn.execute(sql, (category, username, title, author))

            sql = '''
                SELECT category
                FROM user_library
                WHERE (user_id, book_id) = (
                    SELECT user_id, book_id
                    FROM user_books
                    WHERE username=? AND title=? AND author=?
                )
            '''

            row = conn.execute(sql, (username, title, author)).fetchone()

            if not row:
                raise sqlite3.Error('Could not retrieve record from user_library')

            if row['category'] != category:
                raise sqlite3.Error('Could not update category')

        if start_date:
            
            sql = '''
                UPDATE user_library
                SET start_date=?
                WHERE (user_id, book_id) = (
                    SELECT user_id, book_id
                    FROM user_books
                    WHERE username=? AND title=? AND author=?
                )
            '''

            conn.execute(sql, (start_date, username, title, author))

            sql = '''
                SELECT start_date
                FROM user_library
                WHERE (user_id, book_id) = (
                    SELECT user_id, book_id
                    FROM user_books
                    WHERE username=? AND title=? AND author=?
                )
            '''
            row = conn.execute(sql, (username, title, author)).fetchone()
            if not row:
                raise sqlite3.Error('Could not retrieve record from user_library')
            
            if row['start_date'] != start_date:
                raise sqlite3.Error('Could not update start_date')

        if finished_date:
            
            sql = '''
                UPDATE user_library
                SET finished_date=?
                WHERE (user_id, book_id) = (
                    SELECT user_id, book_id
                    FROM user_books
                    WHERE username=? AND title=? AND author=?
                )
            '''

            conn.execute(sql, (finished_date, username, title, author))
            sql = '''
                SELECT finished_date 
                FROM user_library
                WHERE (user_id, book_id) = (
                    SELECT user_id, book_id
                    FROM user_books
                    WHERE username=? AND title=? AND author=?
                )
            '''

            row = conn.execute(sql, (username, title, author)).fetchone()
            if not row:
                raise sqlite3.Error('Could not retrieve record from user_library')
                
            if row['finished_date'] != finished_date:
                raise sqlite3.Error('Could not update finished_date')
        
        sql = '''
            SELECT * 
            FROM user_library
            WHERE (user_id, book_id) = (
                SELECT user_id, book_id
                FROM user_books
                WHERE username=? AND title=? AND author=?
            )
        '''
        
        update = conn.execute(sql, (username, title, author)).fetchone()

        if not update:
            raise sqlite3.Error('Could not retrieve record from user_library')
        
        conn.execute('END TRANSACTION')

        close_db()

        return jsonify({'update' : dict(update), 'reward': reward}), 200
    
    except sqlite3.IntegrityError as e:
        conn.execute('ROLLBACK')
        return jsonify({'error' : str(e)}), 500
    except sqlite3.Error as e:
        conn.execute('ROLLBACK')
        return jsonify({'error' : str(e)}), 500
    except NotFoundError as e:
        return jsonify({'error' : str(e)}), 404
   

@library_bp.post('/<username>/<author>/<title>')
def add_library_book(username, author, title):
    if not username or not author or not title:
        return jsonify({'error' : 'username, author, and title required in url'}), 400

    if not request.is_json:
        return jsonify({'error' : 'request must be JSON object'}), 400

    data = request.get_json()

    status = data.get('status')
    category = data.get('category') or None
    start_date = data.get('start_date') or None
    finished_date = data.get('finished_date') or None

    if not status:
        return jsonify({'error' : 'status is required'}), 422
    
    try:
        
        conn = get_db()
        
        # getting user_id to use for inserting into user_library
        sql = '''
            SELECT user_id 
            FROM users 
            WHERE username=?
        '''

        row = conn.execute(sql, (username,)).fetchone()

        if not row:
            raise NotFoundError('Could not find user')

        user_id = row['user_id']

        # getting book_id to use for inserting into user_library
        sql = '''
            SELECT book_id 
            FROM books 
            WHERE title=? AND author=?
        '''
        row = conn.execute(sql, (title, author)).fetchone()
        
        if not row:
            raise NotFoundError('Could not find book')

        book_id = row['book_id']

        # checking if book is already in user's library
        sql = '''
            SELECT * 
            FROM user_library
            WHERE user_id=? AND book_id=?
        '''
        row = conn.execute(sql, (user_id, book_id)).fetchone()
        if row:
            raise ConflictError('Book already in given user\'s library')
        
        sql = '''
            INSERT INTO user_library
            (user_id, book_id, status, category, start_date, finished_date)
            VALUES
            (?,?,?,?,?,?)
        '''
        conn.execute(sql, (user_id, book_id, status, category, start_date, finished_date))

        sql = '''
            SELECT * 
            FROM user_library 
            WHERE user_id=? AND book_id=?
        '''

        row = conn.execute(sql, (user_id, book_id)).fetchone()

        close_db()

        if not row:
            raise sqlite3.Error('Could not insert book into user_library')
       
        return jsonify(dict(row)), 200
   
    except sqlite3.IntegrityError as e:
        return jsonify({'error' : str(e)}), 500
    except sqlite3.Error as e:
        return jsonify({'error' : str(e)}), 500
    except NotFoundError as e:
        return jsonify({'error' : str(e)}), 404
    except ConflictError as e:
        return jsonify({'error' : str(e)}), 409


@library_bp.get('/<username>/query')
def filter_library(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400
    
    title = request.args.get('title')
    author = request.args.get('author')
    category = request.args.get('category')
    status = request.args.get('status')

    try:
        conn = get_db()
        results = {}

        if title:
            
            sql = '''
                SELECT * 
                FROM user_library AS ul
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
            
            if rows != []:  
                for r in rows:
                    user_id = r['user_id']
                    book_id = r['book_id']
                    results[(user_id, book_id)] = r

        if author:
            sql = '''
                SELECT * 
                FROM user_library AS ul
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
            if rows != []:  
                for r in rows:
                    user_id = r['user_id']
                    book_id = r['book_id']
                    results[(user_id, book_id)] = r
            
        if category:
            sql = '''
                SELECT * 
                FROM user_library AS ul
                JOIN users AS u
                    ON ul.user_id = u.user_id
                WHERE ul.category=? AND u.username=?
            '''
            rows = conn.execute(sql, (category,username)).fetchall()
            
            if rows != []:  
                for r in rows:
                    user_id = r['user_id']
                    book_id = r['book_id']
                    results[(user_id, book_id)] = r

        if status:
            sql = '''
                SELECT * 
                FROM user_library AS ul
                JOIN users AS u
                    ON ul.user_id = u.user_id
                WHERE ul.status=? AND u.username=?
            '''
            rows = conn.execute(sql, (status, username)).fetchall()
            
            if rows != []:  
                for r in rows:
                    user_id = r['user_id']
                    book_id = r['book_id']
                    results[(user_id, book_id)] = r
        
        close_db()

        if len(results) == 0:
            return [], 200

        return jsonify([dict(r) for r in results.values()]), 200

    except sqlite3.Error as e:
        return jsonify({'error' : str(e)}), 500

@library_bp.get('/logs/<username>')
def get_user_reading_logs(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    try:

        conn = get_db()

        sql = '''
            SELECT user_id 
            FROM users 
            WHERE username=?
        '''
        user = conn.execute(sql, (username,)).fetchone()

        if not user:
            NotFoundError('Could not find user')
            
        user_id = user['user_id']

        sql = '''
            SELECT * 
            FROM reading_logs
            WHERE user_id=?
        '''

        rows = conn.execute(sql, (user_id,)).fetchall()

        close_db()
        
        if rows == []:
            return [], 200

        return jsonify([dict(r) for r in rows]), 200

    except sqlite3.Error as e:
        return jsonify({'error' : str(e)}), 500
    except NotFoundError as e:
        return jsonify({'error' : str(e)}), 404

@library_bp.post('/logs/<username>')
def add_reading_log(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    if not request.is_json:
        return jsonify({'error' : 'Request must be a JSON object'}), 400

    log = request.get_json()

    if not log:
        return jsonify({'error' : 'JSON object data is required'}), 400

    book_id = log.get('book_id')
    log_date = log.get('log_date')
    progress = log.get('progress') or None
    notes = log.get('notes') or None
    session_time = log.get('session_time') or None

    if not book_id:
        return jsonify({'error' : 'book_id is required'}), 422
    if not log_date:
        return jsonify({'error' : 'log_date is required'}), 422
    
    try:

        conn = get_db()

        conn.execute('BEGIN TRANSACTION')
        
        sql = '''
            SELECT user_id 
            FROM users 
            WHERE username=?
        '''
        row = conn.execute(sql, (username,)).fetchone()
        if not row:
            raise NotFoundError('Could not find user')
        
        user_id = row['user_id']

        sql = '''
            INSERT INTO reading_logs
            (user_id, book_id, log_date, progress, notes, session_time)
            VALUES
            (?,?,?,?,?,?)
        '''
        cursor = conn.execute(sql, (user_id, book_id, log_date, progress, notes, session_time))
        log_id = cursor.lastrowid
        
        sql = '''
            SELECT log_id
            FROM reading_logs
            WHERE log_id=?
        '''
        row = conn.execute(sql, (log_id,)).fetchone()
        if not row:
            raise sqlite3.Error('Could not insert log into reading_logs')
        
        
        # automatically update book's read status if progress is 100 from log
        if progress == 100:
           
            # checking that book exists in user's library before attempting to update status
            sql = '''
                SELECT status
                FROM user_library
                WHERE user_id=? AND book_id=?
            '''
                       
            row = conn.execute(sql, (user_id, book_id)).fetchone()

            if not row:
                raise NotFoundError('Could not find book in user\'s library')
               
            sql = '''
                UPDATE user_library
                SET status="read"
                WHERE user_id=? AND book_id=?
            '''

            conn.execute(sql, (user_id, book_id))

                        
            if row['status'] != 'read':
                sqlite3.Error('Could not update status')
            
        
        conn.execute('END TRANSACTION')
        close_db()

        if not row:
            return jsonify({'error' : 'log insertion failed'}), 404

        return jsonify(dict(row)), 200

    except sqlite3.IntegrityError as e:
        conn.execute('ROLLBACK')
        return jsonify({'error' : str(e)}), 500
    except sqlite3.Error as e:
        conn.execute('ROLLBACK')
        return jsonify({'error' : str(e)}), 500
    except NotFoundError as e:
        conn.execute('ROLLBACK')
        return jsonify({'error' : str(e)}), 404
    

        
