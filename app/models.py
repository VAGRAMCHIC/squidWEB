import bcrypt

from .database import db
from flask_login import UserMixin


class Users(UserMixin,db.Model):

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password_hash = db.Column(db.String(200))

    def set_password(self, password: str):
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        pwd_bytes = password.encode('utf-8')
        hashed_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)

    def get_id(self):
        return str(self.id)
