from sqlalchemy import ForeignKey, func
from db import db
from models.Group import Group
from models.User import User

class Demand(db.Model):
    __tablename__ = 'demands'

    group_id = db.Column(db.Integer(), ForeignKey(Group.id), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey(User.id), primary_key=True)
    mountain =db.Column(db.Boolean(), nullable=False)
    beach =db.Column(db.Boolean(), nullable=False)
    big_city =db.Column(db.Boolean(), nullable=False)
    village =db.Column(db.Boolean(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())