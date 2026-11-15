from flask import jsonify

def test_get_books(client):
    response = client.get('/books/')
    assert response.status_code == 200
    assert response.json is not None

def test_search_books(client):
    query_title = {
        'title' : 'A Court of Mist and Fury'
    }

    query_author = {
        'author' : 'Sarah J. Maas'
    }

    query_both = {
        'title' : 'Beach Read',
        'author' : 'Emily Henry'
    }

    response1 = client.get('/books/browse', json=query_title)
    assert response1.status_code == 200
    
    response2 = client.get('/books/browse', json=query_author)
    assert response2.status_code == 200

    response3 = client.get('/books/browse', json=query_both)
    assert response3.status_code == 200

    response4 = client.get('/books/browse', json={})
    assert response4.status_code == 400
   
def test_add_book(client):
    book_data = {
        'author' : 'Rebecca Yarros',
        'title' : 'Fourth Wing',
        'publication_year' : 2023,
        'synopsis' : 'Follow the journey of Violet Sorrengail, who is forced to join the Basgiath War college and become a dragon rider in the kingdom of Navarre. Even though she has been trained her entire life to enter the Scribe Quadrant, Violet must endure deadly quests and competitions that push her to her limits while trying to avoid being killed by one of the most powerful riders in the quadrant, Xaden Riorson.',
        'page_count' : 512
    }

    response = client.post('/books/book', json=book_data)

    assert response.status_code == 200

def test_update_book(client):
    book_data = {
        'page_count' : 300
    }

    response = client.put('/books/24', json=book_data)

    assert response.json['page_count'] == book_data['page_count']
    assert response.status_code == 200

def test_get_book_tags(client):
    book_id = 4
    response = client.get(f'/books/{book_id}/tags')

    assert response.status_code == 200

def test_add_book_tag(client):
    book_id = 4
    tag = {
        'tag_name' : 'fiction'
    }

    response = client.post(f'/books/{book_id}/tags', json=tag)
    assert response.status_code == 200
