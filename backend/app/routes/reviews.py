from flask import Blueprint, request, jsonify
from app.db import get_db, close_db
import sqlite3
from app.errors import NotFoundError
from datetime import date

review_bp = Blueprint('review', __name__)

@review_bp.get('/')
def get_all_reviews():
    conn = get_db()

    sql = '''
        SELECT * 
        FROM reviews
        WHERE visibility="public"
        ORDER BY rating DESC
    '''

    reviews = conn.execute(sql).fetchall()

    close_db()

    if reviews == []:
        return jsonify({'error' : 'Could not retrieve all reviews'}), 500

    return jsonify([dict(r) for r in reviews]), 200

@review_bp.get('/book')
def get_book_reviews():
    
    title = request.args.get('title')
    author = request.args.get('author')

    if not title or not author:
        return jsonify({'error' : 'title and author required'}), 400
   
    conn = get_db()
    
    # checking to see if book exists in db
    sql = '''
        SELECT * 
        FROM books
        WHERE title=? AND author=?
    '''
    row = conn.execute(sql, (title, author)).fetchone()
    if row:
        return jsonify({'error' : 'Could not find book in database'}), 404
    
    sql = '''
        SELECT u.username, b.title, b.author, r.review_text, r.rating
        FROM reviews AS r
        JOIN users AS u 
            ON u.user_id = r.user_id 
        JOIN books AS b 
            ON b.book_id = r.book_id 
        WHERE b.author=? AND b.title=? AND visibility="public"
    '''

    reviews = conn.execute(sql, (author, title)).fetchall()

    close_db()
    if not reviews:
        return [], 200

    return jsonify([dict(r) for r in reviews]), 200

@review_bp.get('/user/<username>')
def get_user_reviews(username):
    if not username:
        return jsonify({'error' : 'Username is required'})

    conn = get_db()

    # checking if user exists in db
    sql = '''
        SELECT * 
        FROM users 
        WHERE username=?
    '''
    row = conn.execute(sql, (username,)).fetchone()
    if not row:
        return jsonify({'error' : 'Could not find user'}), 404

    sql = '''
        SELECT r.review_id, u.username, b.title, b.author, r.review_text, r.rating 
        FROM reviews AS r 
        JOIN users AS u 
            ON u.user_id = r.user_id 
        JOIN books AS b 
            ON r.book_id = b.book_id 
        WHERE u.username=? 
        ORDER BY rating DESC
    '''

    reviews = conn.execute(sql, (username,)).fetchall()

    close_db()

    if reviews == []:
        return [], 200

    return jsonify([dict(r) for r in reviews]), 200

@review_bp.post('/user/<username>')
def add_review(username):
    if not username:
        return jsonify({'error' : 'Username is required'}), 400

    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    review_data = request.get_json()

    if not review_data:
        return jsonify({'error' : 'JSON object required'}), 400

    book_id = review_data.get('book_id')
    creation_date = date.today()
    review_text = review_data.get('review_text') or None
    visibility = review_data.get('visibility') or None
    rating = review_data.get('rating')

    if not book_id:
        return jsonify({'error' : 'book_id is required'}), 422
    if not rating:
        return jsonify({'error' : 'rating is required'}), 422
    if not creation_date:
        return jsonify({'error' : 'creation_date is required'}), 422


    try:
                
        conn = get_db()

        # checking if user exists in database before querying
        sql = '''
            SELECT user_id 
            FROM users 
            WHERE username=?
        '''
        user = conn.execute(sql, (username,)).fetchone()
        if not user:
            raise NotFoundError('Could not find user')
        
        user_id = user['user_id']

        # checking if book exists in database before querying
        sql = '''
            SELECT *
            FROM books
            WHERE book_id=?
        '''
        book = conn.execute(sql, (book_id,)).fetchone()
        if not book:
            raise NotFoundError('Could not find book')

        sql = '''
            INSERT INTO reviews
            (user_id, book_id, rating, review_text, visibility, creation_date)
            VALUES
            (?,?,?,?,?, ?)
        '''
        
        cursor = conn.execute(sql, (user_id, book_id, rating, review_text, visibility, creation_date))

        sql = '''
            SELECT * 
            FROM reviews 
            WHERE review_id=?
        '''
        review = conn.execute(sql, (cursor.lastrowid,)).fetchone()
        
        close_db()

        if not review:
            raise sqlite3.Error('Could not insert review')

        return jsonify(dict(review)), 200
    except sqlite3.Error as e:
        return jsonify({'error' : f'Unexpected Error: {str(e)}'}), 500
    except NotFoundError as e:
        return jsonify({'error' : str(e)}), 404
    except Exception as e:
        return jsonify({'error' : f'Something went wrong: {str(e)}'}), 500
