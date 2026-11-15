from app import create_app

def test_app_creation():
    app = create_app({'TESTING' : True,})
    assert app
