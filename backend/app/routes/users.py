from flask import Blueprint, jsonify, request, render_template
from flask import redirect, url_for
from app.db import get_db, close_db
from datetime import date
from app import config

# creating a blueprint instance
user_bp = Blueprint('user', __name__)

@user_bp.get('/')
def get_users():
    conn = get_db()

    sql = 'SELECT * FROM users'

    rows = conn.execute(sql).fetchall()

    close_db()

    if rows is None:
        return jsonify({'error' : 'GET users failed'}), 404

    return jsonify([dict(r) for r in rows]), 200

@user_bp.get('/<username>')
def get_user(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    conn = get_db()

    sql = 'SELECT * FROM users WHERE username=?'
    user = conn.execute(sql, (username,)).fetchone()
    close_db()

    if not user:
        return jsonify({'error' : 'user retrieval failed'}), 404

    return jsonify(dict(user)), 200

# TODO: add get endpoint for signing up that works with front end
@user_bp.get('/login')
def login():
    
    username = request.args.get('username')
    email = request.args.get('email')

    if not username and not email:
        return jsonify({'error' : 'username and email required'}), 400

    # check if user exists and return user_id if they do
    sql = '''
        SELECT * FROM users
        WHERE username=? AND email=?
    '''

    conn = get_db()
    user = conn.execute(sql, (username, email)).fetchone()
    
    close_db()

    if not user:
        return jsonify({'error' : 'user does not exist'}), 404

    return jsonify(dict(user)), 200

# NOTE: this pretty much done for now
@user_bp.post('/signup')
def create_profile():
    
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON'}), 400

    user = request.get_json()
    
    username = user['username']
    first_name = user['first_name']
    last_name = user['last_name']
    email = user['email']
    birth_date = user['birth_date']
    creation_date = date.today()

    errors = {}

    if not username:
        errors['username'] = 'Username is required'

    if not first_name:
        errors['first_name'] = 'First name is required'

    if not last_name:
        errors['last_name'] = 'Last name is required'

    if not email:
        errors['email'] = 'Email is required'

    if not birth_date:
        errors['birth_date'] = 'Birthday is required'

    if len(errors) > 0:
        return jsonify(e for e in errors), 400

    conn = get_db()

    sql = (
        'INSERT INTO users '
        '(username, first_name, last_name, email, birth_date, creation_date) '
        'VALUES (?,?,?,?,?,?)'
    )

    cursor = conn.execute(sql, (username, first_name, last_name,
                                email, birth_date, creation_date))

    sql = (
        'SELECT username, first_name, last_name, email, birth_date, creation_date '
        'FROM users WHERE user_id=?'
    )
    new_user = conn.execute(sql, (cursor.lastrowid,)).fetchone()

    if new_user is None:
        return jsonify({
            'error' : 'Account creation failed'
            }), 404

    conn.close()

    return jsonify(dict(new_user)), 200


# TODO
@user_bp.put('/settings/<username>')
def update_user(username):
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON'}), 400

    user = request.get_json()
    
    first_name = user.get('first_name') or None
    last_name = user.get('last_name') or None
    visibility = user.get('visibility') or None
    
    conn = get_db()

    errors = {}
    
    if first_name:
        sql = (
            'UPDATE users '
            'SET first_name=? '
            'WHERE username=?'
        )

        conn.execute(sql, (first_name, username))
        sql = 'SELECT * FROM users WHERE username=?'
        new_user = conn.execute(sql, (username,)).fetchone()
        
        if new_user['first_name'] != first_name:
            errors['first_name'] = {'error' : 'First name update failed'}
    if last_name:
        sql = (
            'UPDATE users '
            'SET last_name=? '
            'WHERE username=?'
        )

        conn.execute(sql, (last_name, username))
        sql = 'SELECT * FROM users WHERE username=?'

        new_user = conn.execute(sql, (username,)).fetchone()
        if new_user['last_name'] != last_name:
            errors['last_name'] = {'error' : 'Last name update failed!'}

    if visibility:
        sql = (
            'UPDATE users '
            'SET profile_visibility=? '
            'WHERE username=?'
        )

        conn.execute(sql, (visibility, username))
        sql = 'SELECT * FROM users WHERE username=?'

        new_user = conn.execute(sql, (username,)).fetchone()
        if new_user['profile_visibility'] != visibility:
            errors['visibility'] = {'error' : 'Visibility update failed!'}

    sql = 'SELECT * FROM users WHERE username=?'
    new_user = conn.execute(sql, (username,)).fetchone()
    
    close_db()
    
    if len(errors) > 0:
        return jsonify(e for e in errors), 404

    return jsonify(dict(new_user)), 200

@user_bp.delete('/<username>')
def delete_user(username):
    if not username:
        return jsonify({'error' : 'Username is required'}), 400

    conn = get_db()

    sql = (
        'DELETE FROM users '
        'WHERE username=?'
    )

    conn.execute(sql, (username,))
    sql = 'SELECT * FROM users WHERE username=?'
    user = conn.execute(sql, (username,)).fetchone()
    
    if user:
        return jsonify({'error' : 'Account deletion failed'}), 404
    
    close_db()

    return {}, 200

@user_bp.post('/preferences/<username>')
def add_user_preferences(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    preference = request.get_json()

    tag_id = preference['tag_id']
    does_like = preference['does_like']

    if not tag_id or does_like is None:
        return jsonify({'error' : 'tag_id and does_like is required'}), 400

    conn = get_db()

    sql = 'SELECT user_id FROM users WHERE username=?'
    user = conn.execute(sql, (username,)).fetchone()
    
    if not user:
        return jsonify({'error' : 'record retrieval failed'}), 404

    user_id = user['user_id']

    # checking if user has 7 preferences already
    sql = '''
        SELECT COUNT(*) AS num_preferences 
        FROM user_preferences
        WHERE user_id=?
    '''

    row = conn.execute(sql, (user_id,)).fetchone()

    if not row:
        return jsonify({'error' : 'record retrieval failed'}), 404

    current_pref_count = row['num_preferences']
    if current_pref_count >= 7:
        close_db()
        return jsonify({'message' : 'max preferences reached'}), 200

    sql = '''
        INSERT INTO user_preferences
        (user_id, tag_id, does_like)
        VALUES
        (?,?,?)
    '''

    cursor = conn.execute(sql, (user_id, tag_id, does_like))

    sql = 'SELECT * FROM user_preferences WHERE preference_id=?'

    row = conn.execute(sql, (cursor.lastrowid,)).fetchone()

    close_db()

    if not row:
        return jsonify({'error' : 'preference insertion failed'}), 404

    return jsonify(dict(row)), 200

@user_bp.get('/preferences/<username>')
def get_user_preferences(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    conn = get_db()

    sql = '''
        SELECT * FROM user_preferences AS ur
        JOIN users AS u
            ON u.user_id = ur.user_id
        WHERE u.username=?
    '''

    rows = conn.execute(sql, (username,)).fetchall()

    close_db()

    if not rows:
        return jsonify({'message' : 'user has no preferences'}), 200

    return jsonify([dict(r) for r in rows]), 200
