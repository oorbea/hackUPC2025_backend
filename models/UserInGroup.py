from sqlalchemy import ForeignKey, func
from db import db
from models.Group import Group
from models.User import User

class UserInGroup(db.Model):
    __tablename__ = 'useringroups'

    group_id = db.Column(db.Integer(), ForeignKey(Group.id), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey(User.id), primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())

    def to_dict(self):
        """
        Convert the UserInGroup object to a dictionary.
        """
        return {
            'group_id': self.group_id,
            'user_id': self.user_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }