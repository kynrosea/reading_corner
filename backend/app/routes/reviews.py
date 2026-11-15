from flask import Blueprint, request, jsonify
from app.db import get_db, close_db

review_bp = Blueprint('review', __name__)

@review_bp.get('/')
def get_all_reviews():
    conn = get_db()

    sql = (
        'SELECT * FROM reviews '
        'WHERE visibility="public" '
        'ORDER BY rating DESC'
    )

    reviews = conn.execute(sql).fetchall()

    close_db()

    if reviews is None:
        return jsonify({'error' : 'GET public reviews failed'}), 404

    return jsonify([dict(r) for r in reviews]), 200

@review_bp.get('/book')
def get_book_reviews():
    
    title = request.args.get('title')
    author = request.args.get('author')

    if not title or not author:
        return jsonify({'error' : 'title and author required'}), 400
   
    conn = get_db()
    
    sql = (
        'SELECT u.username, b.title, b.author, r.review_text, r.rating '
        'FROM reviews AS r '
        'JOIN users AS u '
        '   ON u.user_id = r.user_id '
        'JOIN books AS b '
        '   ON b.book_id = r.book_id '
        'WHERE b.author=? AND b.title=? AND visibility="public"'
    )

    reviews = conn.execute(sql, (author, title)).fetchall()

    close_db()
    if not reviews:
        return jsonify({'message' : 'No reviews found'}), 200

    return jsonify([dict(r) for r in reviews]), 200

@review_bp.get('/user/<username>')
def get_user_reviews(username):
    if not username:
        return jsonify({'error' : 'Username is required'})

    conn = get_db()

    sql = (
        'SELECT u.username, b.title, b.author, r.review_text, r.rating '
        'FROM reviews AS r '
        'JOIN users AS u '
        '   ON u.user_id = r.user_id '
        'JOIN books AS b '
        '   ON r.book_id = b.book_id '
        'WHERE u.username=? '
        'ORDER BY rating DESC'
    )

    reviews = conn.execute(sql, (username,)).fetchall()

    close_db()

    if not reviews:
        return jsonify({'message' : 'No reviews found'}), 200

    return jsonify([dict(r) for r in reviews]), 200

@review_bp.post('/user/<username>')
def add_review(username):
    if not username:
        return jsonify({'error' : 'Username is required'})

    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'})

    review_data = request.get_json()

    if not review_data:
        return jsonify({'error' : 'JSON object required'}), 400

    book_id = review_data.get('book_id')
    review_text = review_data.get('review_text') or None
    visibility = review_data.get('visibility') or None
    rating = review_data.get('rating')
    
    errors = {}
    
    if not book_id:
        errors['book_id'] = 'book_id required'
    if not rating:
        errors['rating'] = 'rating required'

    if len(errors) > 0:
        return jsonify(e for e in errors), 400

    conn = get_db()

    sql = 'SELECT user_id FROM users WHERE username=?'
    user = conn.execute(sql, (username,)).fetchone()
    user_id = user['user_id']

    sql = 'INSERT INTO reviews (user_id, book_id, rating'
    bindings = [user_id, book_id, rating]
    vals = 3
    if review_text:
        bindings.append(review_text)
        sql += ', review_text'
        vals += 1
    if visibility:
        bindings.append(visibility)
        sql += ', visibility'
        vals += 1
    
    sql += ') VALUES (?'

    for i in range(1,vals):
        sql += ',?'
    
    sql += ')'

    cursor = conn.execute(sql, tuple(bindings))

    sql = 'SELECT * FROM reviews WHERE review_id=?'
    review = conn.execute(sql, (cursor.lastrowid,)).fetchone()

    close_db()

    if not review:
        return jsonify({'error' : 'Review insertion failed'}), 404

    return jsonify(dict(review)), 200

