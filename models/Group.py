from sqlalchemy import func
from db import db

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.Integer(), nullable=False)
    deadline = db.Column(db.DateTime(), nullable=False)
    response = db.Column(db.String(1024), nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())