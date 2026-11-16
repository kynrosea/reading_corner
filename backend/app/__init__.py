import os

from flask import Flask

# importing route blueprints for better endpoint organization
from app.routes.users import user_bp
from app.routes.books import book_bp
from app.routes.reviews import review_bp
from app.routes.library import library_bp
from app.routes.tags import tag_bp
from app.routes.rewards import reward_bp

from app.db import close_db, init_db

def create_app(test_config=None):
    app = Flask(__name__)


    if test_config:
        app.config.update(test_config)
    
    app.teardown_appcontext(close_db)

    app.json.compact = False

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(book_bp, url_prefix='/books')
    app.register_blueprint(review_bp, url_prefix='/reviews')
    app.register_blueprint(library_bp, url_prefix='/library')
    app.register_blueprint(tag_bp, url_prefix='/tags')
    app.register_blueprint(reward_bp, url_prefix='/rewards')
    
    @app.route('/')
    def index():
        return '<h1>Reading Corner</h1>'

    return app
    

