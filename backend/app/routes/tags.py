from flask import Blueprint, request, jsonify
from app.db import get_db, close_db

tag_bp = Blueprint('tag', __name__)

@tag_bp.get('/')
def get_available_tags():
    sql = '''
        WITH tags_intersection AS (
            SELECT tag_id FROM tags
            INTERSECT
            SELECT tag_id FROM book_tags
        )

        SELECT t.tag_name FROM tags AS t
        JOIN tags_intersection AS ti
            ON ti.tag_id = t.tag_id;
     '''

    conn = get_db()

    rows = conn.execute(sql).fetchall()
    
    close_db()

    if not rows:
        return jsonify({'error' : 'GET tags failed'}), 404

    return jsonify([dict(r) for r in rows]), 200


@tag_bp.post('/')
def add_tag():
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    data = request.get_json()

    tag_name = data.get('tag_name')

    conn = get_db()

    sql = '''
        INSERT INTO tags
        (tag_name)
        VALUES
        (?)
    '''

    cursor = conn.execute(sql, (tag_name,))
    sql = 'SELECT * FROM tags WHERE tag_id=?'

    tag = conn.execute(sql, (cursor.lastrowid,)).fetchone()

    close_db()

    if not tag:
        return jsonify({'error' : 'tag insertion failed'}), 404

    return jsonify(dict(tag)), 200


