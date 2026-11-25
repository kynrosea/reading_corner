from flask import Blueprint, jsonify, request
from app.db import get_db, close_db
import sqlite3
from app.errors import ConflictError, NotFoundError, EntityError

# creating a blueprint instance
user_bp = Blueprint('user', __name__)

@user_bp.get('/')
def get_users():
    conn = get_db()

    sql = 'SELECT * FROM users'

    rows = conn.execute(sql).fetchall()

    close_db()

    # the base data has 10+ test users, so this operation should succeed
    # if it fails, then it's a database/sqlite error
    if rows is None:
        return jsonify({'error' : 'Could not retrieve users'}), 500

    return jsonify([dict(r) for r in rows]), 200

@user_bp.get('/<username>')
def get_user(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    conn = get_db()

    sql = '''
        SELECT * 
        FROM users 
        WHERE username=?
    '''
    user = conn.execute(sql, (username,)).fetchone()
    close_db()

    if not user:
        return jsonify({'error' : 'Could not find user'}), 404

    return jsonify(dict(user)), 200

@user_bp.get('/login')
def login():
    
    username = request.args.get('username')
    email = request.args.get('email')

    if not username and not email:
        return jsonify({'error' : 'username and email required'}), 400

    sql = '''
        SELECT * 
        FROM users
        WHERE username=? AND email=?
    '''

    conn = get_db()
    user = conn.execute(sql, (username, email)).fetchone()
    
    close_db()

    if not user:
        return jsonify({'error' : 'Could not find user'}), 404

    return jsonify(dict(user)), 200

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
    creation_date = user['creation_date']

            
    try:
        
        if not username:
            raise EntityError('username is required')
        
        if not first_name:
            raise EntityError('first_name is required')

        if not last_name:
            raise EntityError('last_name is required')

        if not email:
            raise EntityError('email is required')

        if not birth_date:
            raise EntityError('birth_date is required')

        if not creation_date:
            raise EntityError('creation_date is required')

        conn = get_db()

        sql = '''
            SELECT * 
            FROM users
            WHERE username=?
        '''

        row = conn.execute(sql, (username,)).fetchone()
        if row:
            raise ConflictError('User already exists')

        sql = '''
            INSERT INTO users
            (username, first_name, last_name, email, birth_date, creation_date)
            VALUES 
            (?,?,?,?,?,?)
        '''

        conn.execute(sql, (username, first_name, last_name, email, birth_date, creation_date))

        sql = '''
            SELECT *
            FROM users
            WHERE username=?
        '''

        
        new_user = conn.execute(sql, (username,)).fetchone()
        close_db()
        if not user:
            raise sqlite3.Error('Could not insert user')


        return jsonify(dict(new_user)), 200

    except sqlite3.Error as e:
        return jsonify({'error' : f'Unexpected Error: {str(e)}'}), 500
    except EntityError as e:
        return jsonify({'error' : str(e)}), 422
    except ConflictError as e:
        return jsonify({'error' : str(e)}), 409
    except Exception as e:
        return jsonify({'error' : f'Something went wrong: {str(e)}'}), 500


@user_bp.put('/settings/<username>')
def update_user(username):
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON'}), 400

    if not username:
        return jsonify({'error' : 'username is required'}), 400

    data = request.get_json()

    if not data:
        return jsonify({'error' : 'JSON object data is required'}), 400
    
    first_name = data.get('first_name') or None
    last_name = data.get('last_name') or None
    profile_visibility = data.get('profile_visibility') or None
    
    try:
        
        conn = get_db()

        # checking if user exists
        sql = '''
            SELECT *
            FROM users
            WHERE username=?
        '''

        user = conn.execute(sql, (username,)).fetchone()
        if not user:
            raise NotFoundError('Could not find user')

        
        if first_name:
            sql = '''
                UPDATE users
                SET first_name=?
                WHERE username=?
            '''

            conn.execute(sql, (first_name, username))
            sql = 'SELECT * FROM users WHERE username=?'
            new_user = conn.execute(sql, (username,)).fetchone()

            if not new_user:
                raise sqlite3.Error('Could not retrieve user')
            
            if new_user['first_name'] != first_name:
                raise sqlite3.Error('Could not update first_name')
            
        if last_name:
            sql = '''
                UPDATE users
                SET last_name=?
                WHERE username=?
            '''
           
            conn.execute(sql, (last_name, username))
            sql = 'SELECT * FROM users WHERE username=?'
            new_user = conn.execute(sql, (username,)).fetchone()

            if not new_user:
                raise sqlite3.Error('Could not retrieve user')
            
            if new_user['last_name'] != last_name:
                raise sqlite3.Error('Could not update last_name')

        if profile_visibility:
            sql = '''
                UPDATE users
                SET profile_visibility=?
                WHERE username=?
            '''
            
            conn.execute(sql, (profile_visibility, username))
            sql = 'SELECT * FROM users WHERE username=?'
            new_user = conn.execute(sql, (username,)).fetchone()
            
            if not new_user:
                raise sqlite3.Error('Could not retrieve user')
            
            if new_user['profile_visibility'] != profile_visibility:
                raise sqlite3.Error('Could not update profile_visibility')

        sql = 'SELECT * FROM users WHERE username=?'
        new_user = conn.execute(sql, (username,)).fetchone()
        if not new_user:
            raise sqlite3.Error('Could not retrieve user')
        
        close_db()
        
        return jsonify(dict(new_user)), 200
    
    except sqlite3.Error as e:
        return jsonify({'error' : f'Unexpected Error: {str(e)}'}), 500
    except NotFoundError as e:
        return jsonify({'error' : str(e)}), 404
    except Exception as e:
        return jsonify({'error' : f'Something went wrong: {str(e)}'}), 500

@user_bp.delete('/<username>')
def delete_user(username):
    if not username:
        return jsonify({'error' : 'Username is required'}), 400

    try:
        conn = get_db()
        
        # check if user exists before trying to delete
        sql = '''
            SELECT *
            FROM users
            WHERE username=?
        '''
        user = conn.execute(sql, (username,)).fetchone()
        if not user:
            raise NotFoundError('Could not find user')
        
        sql = '''
            DELETE FROM users
            WHERE username=?
        '''
       
        conn.execute(sql, (username,))
        sql = '''
            SELECT *
            FROM users
            WHERE username=?
        '''
        user = conn.execute(sql, (username,)).fetchone()
       
        close_db()
        
        if user:
            raise sqlite3.Error('Could not delete user')
        
        return {}, 200
    
    except sqlite3.Error as e:
        return jsonify({'error' : f'Unexpected Error: {str(e)}'}), 500
    except NotFoundError as e:
        return jsonify({'error' : str(e)}), 404
    except Exception as e:
        return jsonify({'error' : f'Something went wrong: {str(e)}'}), 500

@user_bp.post('/preferences/<username>')
def add_user_preferences(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    preference = request.get_json()

    if not preference:
        return jsonify({'error' : 'JSON object data is required'}), 400

    tag_id = preference.get('tag_id')
    does_like = preference.get('does_like')

    if not tag_id or does_like is None:
        return jsonify({'error' : 'tag_id and does_like is required'}), 422

    try:

        conn = get_db()

        # check if user exists and grab user_id if they do
        sql = '''
            SELECT user_id
            FROM users
            WHERE username=?
        '''

        user = conn.execute(sql, (username,)).fetchone()
        
        if not user:
            raise NotFoundError('Could not find user')

        user_id = user['user_id']

        sql = '''
            SELECT *
            FROM user_preferences
            WHERE user_id=? AND tag_id=?
        '''

        preference = conn.execute(sql, (user_id, tag_id)).fetchone()

        if preference:

            sql = '''
                UPDATE user_preferences
                SET does_like=1
                WHERE user_id=? AND tag_id=?
            '''

            conn.execute(sql, (user_id, tag_id))

            sql = '''
                SELECT *
                FROM user_preferences
                WHERE preference_id=?
            '''

            preference = conn.execute(sql, (preference['preference_id'],)).fetchone()
            
            close_db()
            
            return jsonify(dict(preference)), 200

        sql = '''
            INSERT INTO user_preferences
            (user_id, tag_id, does_like)
            VALUES
            (?,?,?)
        '''

        cursor = conn.execute(sql, (user_id, tag_id, does_like))
        sql = '''
            SELECT *
            FROM user_preferences
            WHERE preference_id=?
        '''

        row = conn.execute(sql, (cursor.lastrowid,)).fetchone()
        
        close_db()
        
        if not row:
            raise sqlite3.Error('Could not insert preference')

        return jsonify(dict(row)), 200
    
    except sqlite3.Error as e:
        return jsonify({'error' : f'Unexpected Error: {str(e)}'}), 500
    except ConflictError as e:
        return jsonify({'error' : str(e)}), 409
    except NotFoundError as e:
        return jsonify({'error' : str(e)}), 404
    except Exception as e:
        return jsonify({'error' : f'Something went wrong: {str(e)}'}), 500

@user_bp.get('/preferences/<username>')
def get_user_preferences(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    try:
        conn = get_db()

        # check if user exists before querying
        sql = '''
            SELECT *
            FROM users
            WHERE username=?
        '''
        user = conn.execute(sql, (username,)).fetchone()
        if not user:
            raise NotFoundError('Could not find user')

        sql = '''
            SELECT * 
            FROM user_preferences AS ur
            JOIN users AS u
                ON u.user_id = ur.user_id
            WHERE u.username=? AND does_like=1
        '''

        rows = conn.execute(sql, (username,)).fetchall()

        close_db()

        if rows == []:
            
            
            return [], 200

        return jsonify([dict(r) for r in rows]), 200
    
    except sqlite3.Error as e:
        return jsonify({'error' : f'Unexpected Error: {str(e)}'}), 500
    except NotFoundError as e:
        return jsonify({'error' : str(e)}), 404
    except Exception as e:
        return jsonify({'error' : f'Something went wrong: {str(e)}'}), 500

@user_bp.delete('/preferences/<username>/<tag_id>')
def delete_user_preference(username, tag_id):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    if not tag_id:
        return jsonify({'error' : 'tag_id is required'}), 400

    conn = get_db()

    sql = '''
        DELETE FROM user_preferences
        WHERE tag_id=?
            AND user_id=(
                SELECT user_id
                FROM users
                WHERE username=?
            )
    '''
    pref = conn.execute(sql, (tag_id, username)).fetchone()

    close_db()

    if pref:
        return jsonify({'error' : 'preference could not be deleted'}), 500

    return jsonify({'message' : 'preference successfully deleted!'}), 200

    

# getting a leaderboard of all public users who have completed at least 2 books in the current year
@user_bp.get('/leaderboard')
def get_leaderboard():
    
    sql = '''
        SELECT u.username, bc.books_completed
        FROM users AS u
        JOIN (
            SELECT user_id, COUNT(*) AS books_completed
            FROM user_library
            WHERE status = "read"
                AND finished_date IS NOT NULL
                AND (finished_date >= "2026-01-01" AND finished_date <= "2026-12-31")
            GROUP BY user_id
            HAVING books_completed >= 2
        ) AS bc
            ON u.user_id = bc.user_id
        WHERE u.profile_visibility = "public"
        ORDER BY bc.books_completed DESC
    '''

    conn = get_db()
    
    rows = conn.execute(sql).fetchall()

    close_db()
    
    if rows == []:
        return [], 200

    return jsonify([dict(r) for r in rows]), 200

