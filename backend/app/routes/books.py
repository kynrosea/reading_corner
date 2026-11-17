from flask import jsonify, request, Blueprint
from app.db import get_db, close_db
import sqlite3
from app.errors import ConflictError, NotFoundError

book_bp = Blueprint('book', __name__)

# get all books currently in the database (books table)
@book_bp.get('/')
def get_all_books():
    
    sql = '''
        SELECT *
        FROM books
        ORDER BY author ASC
    '''
    
    conn = get_db()
    books = conn.execute(sql).fetchall()
    close_db()

    # base data in database has entries for books table
    # if this fails, then it's an sqlite/database error
    if books == []:
        return jsonify({'error' : 'Could not retrieve books!'}), 500

    return jsonify([dict(b) for b in books]), 200

# query all books based on title and author
@book_bp.get('/browse')
def search_books():

    title = request.args.get('title')
    author = request.args.get('author')

    if not title and not author:
        return jsonify({'error' : 'Title or Author required!'}), 400

    conn = get_db()
    books = []

    if title and author:
        sql = '''
            SELECT *
            FROM books
            WHERE LOWER(title)=LOWER(?)
                AND
                LOWER(author)=LOWER(?)
        '''
        books = conn.execute(sql, (title, author)).fetchall()

    elif title:
        sql = '''
            SELECT *
            FROM books
            WHERE LOWER(title)=LOWER(?)
            ORDER BY author ASC
        '''

        books = conn.execute(sql, (title,)).fetchall()

    elif author:
        sql = '''
            SELECT *
            FROM books
            WHERE LOWER(author)=LOWER(?)
            ORDER BY title ASC
        '''

        books = conn.execute(sql, (author,)).fetchall()

    if books is []:
        response = {
            'data' : [],
            'message' : 'No results found!'
        }
        return jsonify(response), 200

    return jsonify([dict(b) for b in books]), 200

# adding a book to database books table
@book_bp.post('/book')
def add_book():
    
    if not request.is_json:
        return jsonify({'error' : 'Request must be a JSON object'}), 400
    
    book = request.get_json()
    if not book:
        return jsonify({'JSON object data is required'}), 400

    author = book.get('author')
    title = book.get('title')
    publication_year = book.get('publication_year')
    synopsis = book.get('synopsis') or None
    isbn = book.get('isbn') or None
    page_count = book.get('page_count') or None
    cover = book.get('cover') or None

    if not author:
        return jsonify({'error' : 'Author is required!'}), 422
    
    if not title:
        return jsonify({'error' : 'Title is required!'}), 422
        
    if not publication_year:
        return jsonify({'error' : 'Publication year is required!'}), 422
    
    try:

        conn = get_db()

        # checking if book is already in database
        # my system doesn't allow for duplicates unlike other systems
        sql = '''
            SELECT *
            FROM books
            WHERE LOWER(title)=LOWER(?) AND LOWER(author)=LOWER(?)
        '''

        book = conn.execute(sql, (title, author)).fetchone()
        if book:
            raise ConflictError('Book already exists!')

        sql = '''
            INSERT INTO books
            (author, title, publication_year, synopsis, isbn, page_count, cover)
            VALUES
            (?,?,?,?,?,?,?)

        '''

        bindings = (author, title, publication_year, synopsis, isbn, page_count, cover)
        cursor = conn.execute(sql, bindings)

        sql = '''
            SELECT *
            FROM books
            WHERE book_id=?
        '''
        book = conn.execute(sql, (cursor.lastrowid,)).fetchone()

        close_db()

        if not book:
            raise sqlite3.Error('Something went wrong: could not add book :(')

        return jsonify(dict(book)), 200
    
    except sqlite3.IntegrityError as e:
        return jsonify({'error' : 'Something went wrong: could not add book :('}), 500
    except sqlite3.Error as e:
        return jsonify({'error' : str(e)}), 500
    except ConflictError as e:
        return jsonify({'error' : str(e)}), 409
    
# deleting book from database
@book_bp.delete('/book')
def delete_book():
    
    title = request.args.get('title')
    author = request.args.get('author')

    if not title and not author:
        return jsonify({'error' : 'title and author required'}), 400

    sql = '''
        DELETE FROM books
        WHERE title=? AND author=?
    '''
    
    conn = get_db()

    conn.execute(sql, (title, author))
    
    sql = '''
        SELECT *
        FROM books
        WHERE title=? AND author=?
    '''
    row = conn.execute(sql, (title, author)).fetchall()
    
    close_db()
    
    if row:
        return jsonify({'error' : 'Could not delete book'}), 500
    
    return [], 200

# updating book information
@book_bp.put('/<book_id>')
def update_book(book_id):
    
    if not book_id:
        return jsonify({'error' : 'book_id is required'}), 400
    
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400
    
    data = request.get_json()

    if not data:
        return jsonify({'error' : 'JSON object data is required'}), 400

    synopsis = data.get('synopsis') or None
    isbn = data.get('isbn') or None
    page_count = data.get('page_count') or None
    cover = data.get('cover') or None

    try:
        
        conn = get_db()

        sql = '''
            SELECT *
            FROM books
            WHERE book_id=?
        '''
        book = conn.execute(sql, (book_id,)).fetchone()
        if not book:
            raise NotFoundError('Could not find book')
        
        conn.execute('BEGIN TRANSACTION')
        
        if synopsis:
            sql = '''
                UPDATE books
                SET synopsis=?
                WHERE book_id=?
            '''
            conn.execute(sql, (synopsis, book_id))
            sql = '''
                SELECT *
                FROM books
                WHERE book_id=?
            '''
            book = conn.execute(sql, (book_id,)).fetchone()
            if book['synopsis'] != synopsis:
                raise sqlite3.Error('Could not update synopsis')

        if isbn:
            sql = '''
                UPDATE books
                SET isbn=?
                WHERE book_id=?
            '''
            conn.execute(sql, (isbn, book_id))
            sql = '''
                SELECT *
                FROM books
                WHERE book_id=?
            '''
            book = conn.execute(sql, (book_id,)).fetchone()
            if book['isbn'] != isbn:
                raise sqlite3.Error('Could not update ISBN')

        if page_count:
            sql = '''
                UPDATE books
                SET page_count=?
                WHERE book_id=?
            '''
            conn.execute(sql, (page_count, book_id))
            sql = '''
                SELECT *
                FROM books
                WHERE book_id=?
            '''
            book = conn.execute(sql, (book_id,)).fetchone()
            if book['page_count'] != page_count:
                raise sqlite3.Error('Could not update page count')

        if cover:
            sql = '''
                UPDATE books
                SET cover=?
                WHERE book_id=?
            '''
            conn.execute(sql, (cover, book_id))
            sql = '''
                SELECT *
                FROM books
                WHERE book_id=?
            '''
            book = conn.execute(sql, (book_id,)).fetchone()
            if book['cover'] != cover:
                raise sqlite3.Error('Could not update cover')

        book = conn.execute('SELECT * FROM books WHERE book_id=?', (book_id,)).fetchone()

        conn.execute('END TRANSACTION')

        close_db()

        if not book:
            raise sqlite3.Error('Could not retrieve book')
        
        return jsonify(dict(book)), 200
    
    except sqlite3.IntegrityError as e:
        conn.execute('ROLLBACK')
        return jsonify({'error' : str(e)}), 500
    except sqlite3.Error as e:
        conn.execute('ROLLBACK')
        return jsonify({'error' : str(e)}), 500
    except NotFoundError as e:
        return jsonify({'error' : str(e)}), 404
    
# getting all tags associated with a book
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

    if rows == []:
        response = {
            'data' : [],
            'message' : 'This book has no tags'
        }
        return jsonify(response), 200

    return jsonify([dict(r) for r in rows]), 200

# adding a tag to associate with book
@book_bp.post('/<book_id>/tags')
def add_book_tag(book_id):
    if not book_id:
        return jsonify({'error' : 'book_id is required'}), 400

    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    tag = request.get_json()

    if not tag:
        return jsonify({'error' : 'JSON object data is required'})

    tag_name = tag.get('tag_name')
    
    if not tag_name:
        return jsonify({'error' : 'A tag name is required!'}), 422

    conn = get_db()

    sql = 'SELECT tag_id FROM tags WHERE tag_name=?'

    row = conn.execute(sql, (tag_name,)).fetchone()
    if not row:
        return jsonify({'error' : 'Could not find tag'}), 404

    tag_id = row['tag_id']

    sql = '''
        INSERT INTO book_tags
        (book_id, tag_id)
        VALUES
        (?,?)
    '''
    cursor = conn.execute(sql, (book_id, tag_id))
    sql = '''
        SELECT b.book_id, t.tag_name
        FROM tags AS t
        JOIN book_tags AS bt
            ON bt.tag_id = t.tag_id
        WHERE book_id=? AND tag_id=?
    '''
    row = conn.execute(sql, (book_id, tag_id)).fetchone()

    close_db()

    if not row:
        return jsonify({'error' : 'Could not insert book'}), 500

    return jsonify(dict(row)), 200
    
