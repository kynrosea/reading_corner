from flask import jsonify

def test_get_reviews(client):
    response = client.get('/reviews/')
    
    assert response.json != None
    assert response.status_code == 200

def test_get_book_reviews(client):
    book_data = {
        'title' : 'Beach Read',
        'author' : 'Emily Henry'
    }

    response = client.get('/reviews/book', json=book_data)

    assert response.status_code == 200

def test_get_user_reviews(client):
    username = 'itzzzYUNA'
    response = client.get(f'/reviews/user/{username}')

    assert response.status_code == 200
    
