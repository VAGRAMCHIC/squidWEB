import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    # Создание таблиц при первом запуске
    with app.app_context():
        db.create_all()
        
