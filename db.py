from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    picture = db.Column(db.String(200), nullable=True)
    reset_code = db.Column(db.Integer(), nullable=True)
    reset_code_expiration = db.Column(db.DateTime(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"<User {self.username}>"
