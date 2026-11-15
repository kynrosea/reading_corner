from app.db import get_db, close_db
from flask import jsonify
from datetime import date

def test_get_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    
def test_insert_user(client, app):

    user = {
        'username' : 'akyra_rose',
        'first_name' : 'Kyra',
        'last_name' : 'Rose',
        'email' : 'kyn.rose17@gmail.com',
        'birth_date' : '2003-05-23',
        'creation_date' : str(date.today())
    }

    response = client.post('/users/signup', json=user)


    assert response.json == user
    
    assert response.status_code == 200

def test_update_user(client):
    response = client.put('/users/settings/itzzzYUNA', json={
        'visibility' : 'private'
    })
    
    assert response.json.get('profile_visibility') == 'private'

    assert response.status_code == 200

def test_delete_user(client):
    username='itzzzYUNA'

    response = client.delete(f'/users/{username}')

    assert response.status_code == 200

def test_get_preferences(client):
    username='itzzzYUNA'
    
    response = client.get(f'/users/preferences/{username}')

    assert response.status_code == 200

def test_add_preference(client):
    username='itzzzYUNA'

    preference = {
        'tag_id' : 7,
        'does_like' : 1
    }

    response = client.post(f'/users/preferences/{username}', json=preference)

    assert response.status_code == 200
