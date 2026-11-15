from flask import Blueprint, jsonify, request
from app.db import get_db, close_db
from app.util import build_sql_statement

reward_bp = Blueprint('reward', __name__)

@reward_bp.get('/')
def get_all_rewards():
    sql = '''
        SELECT * FROM all_user_rewards;
    '''

    conn = get_db()

    rows = conn.execute(sql).fetchall()

    close_db()

    if not rows:
        return jsonify({'error' : 'GET rewards failed'}), 404

    return jsonify([dict(r) for r in rows]), 200

@reward_bp.get('/<username>')
def get_user_rewards(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400

    sql = '''
        SELECT * FROM all_user_rewards
        WHERE username=?
    '''

    conn = get_db()

    rows = conn.execute(sql, (username,)).fetchall()

    close_db()

    if not rows:
        return jsonify({'message' : 'user has no rewards'}), 404

    return jsonify([dict(r) for r in rows]), 200

@reward_bp.post('/<username>')
def add_user_reward(username):
    if not username:
        return jsonify({'error' : 'username is required'}), 400
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'error' : 'JSON object data required'}), 400

    reward_id = data.get('reward_id')

    if not reward_id:
        return jsonify({'error' : 'reward_id is required'}), 400

    conn = get_db()
    
    sql = 'SELECT user_id FROM users WHERE username=?'
    user = conn.execute(sql, (username,)).fetchone()
    user_id = user['user_id']

    sql = '''
        INSERT INTO user_rewards (user_id, reward_id)
        VALUES (?,?)
        ON CONFLICT (user_id, reward_id)
        DO UPDATE
            SET duplicate_count=duplicate_count+1
    '''
    
    conn.execute(sql, (user_id, reward_id))

    sql = 'SELECT * FROM user_rewards WHERE user_id=? AND reward_id=?'

    row = conn.execute(sql, (user_id, reward_id)).fetchone()

    close_db()

    if not row:
        return jsonify({'error' : 'reward insertion failed'}), 404

    return jsonify(dict(row)), 200

@reward_bp.post('/')
def add_reward():
    if not request.is_json:
        return jsonify({'error' : 'Request must be JSON object'}), 400

    reward = request.get_json()

    if not reward:
        return jsonify({'error' : 'JSON object data required'}), 400

    species = reward.get('species')
    rarity = reward.get('rarity')
    image = reward.get('image') or None
    description = reward.get('description') or None

    if not species or not rarity:
        return jsonify({'error' : 'species and rarity are required'}), 400

    conn = get_db()
    
    sql, bindings = build_sql_statement(
            'rewards',
            [species, rarity],
            ['species', 'rarity'],
            2,
            [image, description],
            ['image', 'description']
    )

    cursor = conn.execute(sql, tuple(bindings))
    sql = 'SELECT * FROM rewards WHERE reward_id=?'
    row = conn.execute(sql, (cursor.lastrowid,)).fetchone()

    close_db()

    if not row:
        return jsonify({'error' : 'reward insertion failed'}), 404

    return jsonify(dict(row)), 200

@reward_bp.get('/leaderboard')
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
    
    if not rows:
        return jsonify({'error' : 'GET leaderboard failed'}), 404

    return jsonify([dict(r) for r in rows]), 200


