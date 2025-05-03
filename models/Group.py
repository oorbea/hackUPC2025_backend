from sqlalchemy import func
from db import db
from schemas import GroupResponseSchema

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    code = db.Column(db.Integer(), nullable=False)
    deadline = db.Column(db.DateTime(), nullable=False)
    response = db.Column(db.String(1024), nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())

    def to_dict(self) -> GroupResponseSchema:
        """
        Convert the Group object to a dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'deadline': self.deadline.strftime('%Y-%m-%d %H:%M:%S'),
            'response': self.response,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }