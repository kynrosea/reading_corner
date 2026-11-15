from flask import jsonify

def test_get_all_rewards(client):
    response = client.get('/rewards/')

    assert response.status_code == 200

def test_get_user_rewards(client):
    username = 'itzzzYUNA'
    response = client.get(f'/rewards/{username}')
    assert response.status_code == 200

def test_add_user_reward(client):
    username = 'itzzzYUNA'

    data = {
        'reward_id' : 12
    }

    response = client.post(f'/rewards/{username}', json=data)

    assert response.status_code == 200

def test_add_reward(client):
    data = {
        'species' : 'balkan marbled white',
        'rarity' : 'uncommon',
    }

    response = client.post('/rewards/', json=data)

    assert response.status_code == 200

def test_get_leaderboard(client):
    response = client.get('/rewards/leaderboard')
    assert response.status_code == 200
