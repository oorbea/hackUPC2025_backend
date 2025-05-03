from db import db

class Demand(db.Model):
    __tablename__ = 'demands'

    group_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), primary_key=True)
    mountain =db.Column(db.Boolean(), nullable=False)
    beach =db.Column(db.Boolean(), nullable=False)
    big_city =db.Column(db.Boolean(), nullable=False)
    village =db.Column(db.Boolean(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(500), nullable=False)