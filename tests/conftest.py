import pytest
from app import create_app
from app.db import get_db, init_db

# creating isolated db file for each test function
@pytest.fixture
def app(tmp_path):
    db_path = tmp_path / 'test.sqlite'

    app = create_app({
        'TESTING' : True,
        'DATABASE' : str(db_path)
    })

    # create tables and insert baseline data
    # will be the same for each test without interfering with one another
    with app.app_context(): # initializing schema
    
        init_db()
    
        yield app


@pytest.fixture
def client(app):
    return app.test_client()
