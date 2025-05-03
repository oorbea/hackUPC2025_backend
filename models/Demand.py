from sqlalchemy import ForeignKey, func
from db import db
from models.Group import Group
from models.User import User
from schemas import DemandResponseSchema

class Demand(db.Model):
    __tablename__ = 'demands'

    group_id = db.Column(db.Integer(), ForeignKey(Group.id), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey(User.id), primary_key=True)
    mountain = db.Column(db.Boolean(), nullable=False)
    beach = db.Column(db.Boolean(), nullable=False)
    big_city = db.Column(db.Boolean(), nullable=False)
    village = db.Column(db.Boolean(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    def to_dict(self) -> dict:
        """
        Convert the Demand object to a dictionary.
        """
        return {
            'group_id': self.group_id,
            'user_id': self.user_id,
            'mountain': self.mountain,
            'beach': self.beach,
            'big_city': self.big_city,
            'village': self.village,
            'price': self.price,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }