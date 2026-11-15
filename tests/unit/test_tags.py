from flask import jsonify

def test_get_available_tags(client):
    response = client.get('/tags/')

    assert response.status_code == 200

def test_add_tag(client):
    tag = {
        'tag_name' : 'psychological thriller'
    }

    response = client.post('/tags/', json=tag)

    assert response.status_code == 200
