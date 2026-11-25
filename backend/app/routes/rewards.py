from flask import Blueprint, jsonify, request
from app.db import get_db, close_db
import sqlite3
from app.errors import ConflictError, NotFoundError

reward_bp = Blueprint('reward', __name__)

@reward_bp.get('/')
def get_all_rewards():
    sql = '''
        SELECT *
        FROM rewards
    '''

    conn = get_db()
    
    rows = conn.execute(sql).fetchall()

    # base data in database has entries for the rewards table
    # if this fails, it's an sqlite/database error
    if rows == []:
        return jsonify({'error' : 'Could not retrieve rewards'}), 500

    return jsonify([dict(r) for r in rows]), 200

# get all rewards across all users
@reward_bp.get('/users')
def get_all_user_rewards():
    
    sql = '''
        SELECT * 
        FROM all_user_rewards;
    '''

    conn = get_db()

    rows = conn.execute(sql).fetchall()

    close_db()

    # base data has entries for rewards table
    # this should succeed; if not, then it's a database/sqlite error
    if not rows:
        return jsonify({'error' : 'Could not retrieve rewards'}), 500

    return jsonify([dict(r) for r in rows]), 200

# get all user's rewards from user_rewards
@reward_bp.get('/<username>')
def get_user_rewards(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    try:
        conn = get_db()

        # check that user exists before querying user_rewards
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
            FROM all_user_rewards
            WHERE username=?
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

# add reward to user_rewards table
@reward_bp.post('/<username>')
def add_user_reward(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    reward = request.get_json()
    
    if not reward:
        return jsonify({'error' : 'JSON object data is required'}), 400

    reward_id = reward.get('reward_id')

    if not reward_id:
        return jsonify({'error' : 'reward_id is required'}), 400

    try:

        conn = get_db()

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
            INSERT INTO user_rewards 
            (user_id, reward_id)
            VALUES (?,?)
            ON CONFLICT (user_id, reward_id)
            DO UPDATE
                SET duplicate_count=duplicate_count+1
        '''
        
        conn.execute(sql, (user_id, reward_id))

        sql = '''
            SELECT *
            FROM user_rewards
            WHERE user_id=? AND reward_id=?
        '''

        row = conn.execute(sql, (user_id, reward_id)).fetchone()

        close_db()

        if not row:
            raise sqlite3.Error('Could not insert user\'s reward')

        return jsonify(dict(row)), 200
    
    except sqlite3.Error as e:
        return jsonify({'error' : f'Unexpected Error: {str(e)}'}), 500
    except NotFoundError as e:
        return jsonify({'error' : str(e)}), 404
    except Exception as e:
        return jsonify({'error' : f'Something went wrong: {str(e)}'}), 500
    
# add reward to rewards table
@reward_bp.post('/')
def add_reward():
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    reward = request.get_json()

    if not reward:
        return jsonify({'error' : 'JSON object data is required'}), 400

    species = reward.get('species')
    rarity = reward.get('rarity')
    image = reward.get('image') or None
    description = reward.get('description') or None

    if not species or not rarity:
        return jsonify({'error' : 'species and rarity are required'}), 422

    try:
        conn = get_db()

        # check if reward has already been added to database
        sql = '''
            SELECT *
            FROM rewards
            WHERE species=?
        '''
        reward = conn.execute(sql, (species,)).fetchone()
        if reward:
            raise ConflictError('Reward with this species already exists in rewards table')

        sql = '''
            INSERT INTO rewards
            (species, rarity, image, description)
            VALUES
            (?,?,?,?)
        '''

        cursor = conn.execute(sql, (species, rarity, image, description))
        
        sql = '''
            SELECT *
            FROM rewards
            WHERE reward_id=?
        '''
        row = conn.execute(sql, (cursor.lastrowid,)).fetchone()
        
        
        close_db()

        if not row:
            return jsonify({'error' : 'reward insertion failed'}), 404

        return jsonify(dict(row)), 200
    
    except sqlite3.Error as e:
        return jsonify({'error' : f'Unexpected Error: {str(e)}'}), 500
    except ConflictError as e:
        return jsonify({'error' : str(e)}), 409
    except Exception as e:
        return jsonify({'error' : f'Something went wrong: {str(e)}'}), 500

# allows a user to randomly obtain a reward through the wish system
# the logic for the wish system, including rules/constraints is written here
@reward_bp.put('/wish/<username>')
def wish(username):
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
            raise NotFoundError('Could not find user')
        
        user_id = user['user_id']
    
        # this whole process is a transaction since we're updating values and inserting entries
        # if one part fails, the whole transaction fails and will be rolled back
        conn.execute('BEGIN TRANSACTION')
        
        sql = '''
            SELECT leaf_balance 
            FROM users
            WHERE username=?
        '''

        row = conn.execute(sql, (username,)).fetchone()
        initial_leaf_balance = row['leaf_balance']
        
        # cannot obtain a new reward if leaf balance is too low
        if initial_leaf_balance < 100:
            response = {
                'reward' : [],
                'remaining_leaves' : initial_leaf_balance
            }
            
            return jsonify(response), 200

        # order by random() puts the rows in a random order
        # limit 1 only returns one row
        # this simulates obtaining a random entry
        sql = '''
            SELECT * 
            FROM rewards
            ORDER BY RANDOM()
            LIMIT 1
        '''

        reward = conn.execute(sql).fetchone()
        if not reward:
            raise sqlite3.Error('Could not retrieve reward')

        reward_id = reward['reward_id']
        
        # need to update the user's leaf_balance since they've made a successful wish
        sql = '''
            UPDATE users
            SET leaf_balance=leaf_balance-100
            WHERE username=?
        '''

        conn.execute(sql, (username,))

        sql = '''
            SELECT *
            FROM users
            WHERE username=?
        '''
        user = conn.execute(sql, (username,)).fetchone()

        leaf_balance = user['leaf_balance']
        if leaf_balance == initial_leaf_balance:
            raise sqlite3.Error('Could not update leaf_balance')
        
        # increasing number of duplicates if user already has rewards in user_rewards
        sql = '''
            INSERT INTO user_rewards 
            (user_id, reward_id)
            VALUES (?,?)
            ON CONFLICT (user_id, reward_id)
            DO UPDATE
                SET duplicate_count=duplicate_count+1
        '''

        conn.execute(sql, (user_id, reward_id))
        sql = '''
            SELECT *
            FROM user_rewards
            WHERE user_id=? AND reward_id=?
        '''
        user_reward = conn.execute(sql, (user_id, reward_id)).fetchone()

        if not user_reward:
            raise sqlite3.Error('Could not insert user\'s reward into user_rewards table')
        
        conn.execute('END TRANSACTION');

        close_db()
        
        return jsonify({'reward' : dict(reward), 'remaining_leaves' : leaf_balance}), 200

    except sqlite3.Error as e:
        conn.execute('ROLLBACK')
        return jsonify({'error' : f'Unexpected Error: {str(e)}'}), 500
    except NotFoundError as e:
        return jsonify({'error' : str(e)}), 404
    except Exception as e:
        conn.execute('ROLLBACK')
        return jsonify({'error' : f'Something went wrong: {str(e)}'}), 500


