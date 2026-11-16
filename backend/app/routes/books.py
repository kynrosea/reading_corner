from flask import jsonify, request, Blueprint
from app.db import get_db, close_db
from app import config
from app.util import build_sql_statement

book_bp = Blueprint('book', __name__)

@book_bp.get('/')
def get_all_books():
    sql = 'SELECT * FROM books'
    conn = get_db()
    books = conn.execute(sql).fetchall()
    close_db()

    if books is None:
        return jsonify({'error' : 'GET books failed'}), 404

    return jsonify([dict(b) for b in books]), 200

@book_bp.get('/browse')
def search_books():

    title = request.args.get('title')
    author = request.args.get('author')

    if not title and not author:
        return jsonify({'error' : 'title or author required'}), 400

    conn = get_db()
    books = None

    if title and author:
        sql = 'SELECT * FROM books WHERE LOWER(title)=LOWER(?) AND LOWER(author)=LOWER(?)'
        books = conn.execute(sql, (title, author)).fetchall()

    elif title:
        sql = (
            'SELECT * FROM books '
            'WHERE LOWER(title)=LOWER(?)'
        )

        books = conn.execute(sql, (title,)).fetchall()

    elif author:
        sql = (
            'SELECT * FROM books '
            'WHERE LOWER(author)=LOWER(?)'
        )

        books = conn.execute(sql, (author,)).fetchall()

    if books is []:
        return jsonify({'message' : 'No results found'}), 200

    return jsonify([dict(b) for b in books]), 200

@book_bp.post('/book')
def add_book():
    book = request.get_json()

    author = book.get('author')
    title = book.get('title')
    publication_year = book.get('publication_year')
    synopsis = book.get('synopsis') or None
    isbn = book.get('isbn') or None
    page_count = book.get('page_count') or None
    cover = book.get('cover') or None

    errors = {}

    if not author:
        errors['author'] = 'Author is required'
    if not title:
        errors['title'] = 'Title is required'
    if not publication_year:
        errors['publication_year'] = 'Publication year is required'

    if len(errors) > 0:
        return jsonify([e for e in errors]), 400


    conn = get_db()

    sql = '''
        INSERT INTO books
        (author, title, publication_year, synopsis, isbn, page_count, cover)
        VALUES
        (?,?,?,?,?,?,?)

    '''

    bindings = (author, title, publication_year, synopsis, isbn, page_count, cover)
    cursor = conn.execute(sql, bindings)
    sql = 'SELECT * FROM books WHERE book_id=?'
    new_book = conn.execute(sql, (cursor.lastrowid,)).fetchone()

    close_db()

    if new_book is None:
        return jsonify({'error' : 'Book insertion failed'}), 404

    return jsonify(dict(new_book)), 200

@book_bp.delete('/book')
def delete_book():
    
    title = request.args.get('title')
    author = request.args.get('author')

    if not title and not author:
        return jsonify({'error' : 'title and author required'}), 400
    
    sql = 'DELETE FROM books WHERE title=? AND author=?'
    conn = get_db()

    conn.execute(sql, (title, author))
    sql = 'SELECT * FROM books WHERE title=? AND author=?'
    row = conn.execute(sql, (title, author)).fetchall()
    close_db()
    
    if row:
        return jsonify({'error' : 'book deletion failed'}), 404
    
    return [], 200

@book_bp.put('/<book_id>')
def update_book(book_id):
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400
    
    data = request.get_json()

    if data is None:
        return jsonify({'error' : 'JSON object data required'}), 400

    synopsis = data.get('synopsis') or None
    isbn = data.get('isbn') or None
    page_count = data.get('page_count') or None
    cover = data.get('cover') or None

    conn = get_db()
    
    if synopsis:
        sql = 'UPDATE books SET synopsis=? WHERE book_id=?'
        conn.execute(sql, (synopsis, book_id))

    if isbn:
        sql = 'UPDATE books SET isbn=? WHERE book_id=?'
        conn.execute(sql, (isbn, book_id))

    if page_count:
        sql = 'UPDATE books SET page_count=? WHERE book_id=?'
        conn.execute(sql, (page_count, book_id))

    if cover:
        sql = 'UPDATE books SET cover=? WHERE book_id=?'
        conn.execute(sql, (cover, book_id))

    book = conn.execute('SELECT * FROM books WHERE book_id=?', (book_id,)).fetchone()

    close_db()
    
    if book is None:
        return jsonify({'error' : 'Book not found; Update failed'}), 404

    return jsonify(dict(book)), 200

@book_bp.get('/<book_id>/tags')
def get_book_tags(book_id):
    if not book_id:
        return jsonify({'error' : 'book_id is required'}), 400

    conn = get_db()

    sql = '''
        SELECT t.tag_name, t.tag_id
        FROM tags AS t
        JOIN book_tags AS bt
            ON bt.tag_id = t.tag_id
        WHERE bt.book_id=?
    '''

    rows = conn.execute(sql, (book_id,)).fetchall()

    close_db()

    if not rows:
        return jsonify({'message' : 'this book has no tags'}), 200

    return jsonify([dict(r) for r in rows]), 200

@book_bp.post('/<book_id>/tags')
def add_book_tag(book_id):
    if not book_id:
        return jsonify({'error' : 'book_id is required'}), 400

    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    tag = request.get_json()

    if not tag:
        return jsonify({'error' : 'JSON object data is required'})

    tag_name = tag['tag_name']
    
    if not tag_name:
        return jsonify({'error' : 'tag_name is required'}), 400

    conn = get_db()

    sql = 'SELECT tag_id FROM tags WHERE tag_name=?'

    row = conn.execute(sql, (tag_name,)).fetchone()
    if not row:
        return jsonify({'error' : 'record retrieval failed'}), 404

    tag_id = row['tag_id']

    sql = '''
        INSERT INTO book_tags
        (book_id, tag_id)
        VALUES
        (?,?)
    '''
    cursor = conn.execute(sql, (book_id, tag_id))
    sql = 'SELECT * FROM book_tags WHERE book_id=? AND tag_id=?'
    row = conn.execute(sql, (book_id, tag_id)).fetchone()

    close_db()

    if not row:
        return jsonify({'error' : 'book tag insertion failed'}), 404

    return jsonify(dict(row)), 200

    


    
