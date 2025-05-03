from sqlalchemy import ForeignKey, func
from db import db
from models.Group import Group
from models.User import User

class UserInGroup(db.Model):
    __tablename__ = 'userInGroups'

    group_id = db.Column(db.Integer(), ForeignKey(Group.id), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey(User.id), primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())