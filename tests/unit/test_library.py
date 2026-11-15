from flask import jsonify

def test_get_library(client):
    username = 'itzzzYUNA'
    response = client.get(f'/library/{username}')

    assert response.status_code == 200

def test_update_library(client):
    username = 'itzzzYUNA'
    title = 'Beach Read'
    author = 'Emily Henry'

    update_data = {
        'category' : 'personal',
        'finished_date' : '2026-11-03'
    }

    response = client.put(f'/library/{username}/{author}/{title}', json=update_data)

    assert response.status_code == 200

def test_add_user_book(client):
    username = 'itzzzYUNA'
    title = 'They Wish They Were Us'
    author = 'Jessica Goodman'
    
    data = {
        'status' : 'currently reading',
        'start_date' : '2026-11-12'
    }

    response = client.post(f'/library/{username}/{author}/{title}', json=data)

    assert response.status_code == 200

def test_library_query(client):
    username = 'itzzzYUNA'

    data = {
        'author' : 'Sarah J. Maas',
        'status' : 'read'
    }

    response = client.get(f'/library/{username}/query', json=data)

    assert response.status_code == 200
    assert response.json is not None

def test_get_reading_logs(client):
    username = 'mchen'

    response = client.get(f'/library/logs/{username}')

    assert response.status_code == 200

def test_add_reading_log(client):
    username = 'mchen'
    
    log_data = {
        'book_id' : 'currently reading',
        'progress' : 100,
    }
    
    response = client.get(f'/library/logs/{username}', json=log_data)

    assert response.status_code == 200
    
