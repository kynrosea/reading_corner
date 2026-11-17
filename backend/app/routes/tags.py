from flask import Blueprint, request, jsonify
from app.db import get_db, close_db
import sqlite3
from app.errors import ConflictError

tag_bp = Blueprint('tag', __name__)

@tag_bp.get('/')
def get_available_tags():
    sql = '''
        WITH tags_intersection AS (
            SELECT tag_id 
            FROM tags
            INTERSECT
            SELECT tag_id FROM book_tags
        )

        SELECT t.tag_name 
        FROM tags AS t
        JOIN tags_intersection AS ti
            ON ti.tag_id = t.tag_id;
     '''

    conn = get_db()

    rows = conn.execute(sql).fetchall()
    
    close_db()

    # if there are no available tags, then sqlite query failed
    # the base data in the database has available tags so this should always succeed if the sql is correct
    if rows == []:
        return jsonify({'error' : 'Could not retrieve available tags'}), 500

    return jsonify([dict(r) for r in rows]), 200


@tag_bp.post('/')
def add_tag():
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    data = request.get_json()

    tag_name = data.get('tag_name')

    try:
        
        conn = get_db()

        # checking if tag is already in the tags table
        sql = '''
            SELECT * 
            FROM tags
            WHERE tag_name=?
        '''
        row = conn.execute(sql, (tag_name,)).fetchone()
        if row:
            raise ConflictError('tag is already in tags table')

        sql = '''
            INSERT INTO tags
            (tag_name)
            VALUES
            (?)
        '''

        conn.execute(sql, (tag_name,))
        
        sql = '''
            SELECT * 
            FROM tags 
            WHERE tag_name=?
        '''

        tag = conn.execute(sql, (tag_name,)).fetchone()

        close_db()

        if not tag:
            raise sqlite3.Error('Could not insert tag')

        return jsonify(dict(tag)), 200
    
    except sqlite3.Error as e:
        return jsonify({'error' : str(e)}), 500
    except sqlite3.Error as e:
        return jsonify({'error' : str(e)}), 500
    except ConflictError as e:
        return jsonify({'error' : str(e)}), 409


