from random import randint
from flask import abort, jsonify
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint
from marshmallow import ValidationError
from psycopg2 import IntegrityError

from db import db
from models.Group import Group
from models.User import User
from models.UserInGroup import UserInGroup
from schemas import EnterGroupSchema, GroupPayloadSchema, GroupResponseSchema

blp = Blueprint('group', __name__, description='Group related CRUD operations.')

@blp.route('')
class GroupCRUD(MethodView):
    """
    Group CRUD operations.
    """
    @jwt_required()
    @blp.doc(security=[{"jwt": []}])
    @blp.arguments(GroupPayloadSchema)
    @blp.response(201, GroupResponseSchema)
    @blp.response(400, description="Bad request.")
    @blp.response(409, description="Conflict.")
    @blp.response(500, description="Internal server error.")
    def post(self, data):
        """
        Create a new group.
        """
        try:
            data['code'] = randint(10000000, 99999999)
            group = Group(**data)

            db.session.add(group)
            db.session.commit()

            user_id = int(get_jwt_identity())
            user:User = User.query.get(user_id)
            if user is None:
                abort(404, message="User not found.")

            user_in_group = UserInGroup(group_id=group.id, user_id=user.id)

            db.session.add(user_in_group)
            db.session.commit()

            return jsonify(group.to_dict()), 201
        except ValidationError as e:
            abort(400, message=str(e))
        except IntegrityError as e:
            db.session.rollback()
            abort(409, message=str(e.orig))
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal server error.")

    @jwt_required()
    @blp.doc(security=[{"jwt": []}])
    @blp.response(200, GroupResponseSchema(many=True))
    @blp.response(400, description="Bad request.")
    @blp.response(404, description="Not found.")
    @blp.response(500, description="Internal server error.")
    def get(self):
        """
        Get logged in user's groups.
        """
        try:
            user_id = int(get_jwt_identity())
            user:User = User.query.get(user_id)
            if user is None:
                abort(404, message="User not found.")

            groups = db.session.query(Group).join(UserInGroup).filter(UserInGroup.user_id == user.id).all()

            return jsonify([group.to_dict() for group in groups]), 200
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal server error.")

@blp.route('/enter')
class EnterGroup(MethodView):
    """
    Endpoint to enter a group using a code.
    """
    @jwt_required()
    @blp.doc(security=[{"jwt": []}])
    @blp.arguments(EnterGroupSchema)
    @blp.response(200, GroupResponseSchema)
    @blp.response(400, description="Bad request.")
    @blp.response(404, description="Not found.")
    @blp.response(409, description="Conflict.")
    @blp.response(500, description="Internal server error.")
    def post(self, data):
        """
        Enter a group using a code.
        """
        try:
            user_id = int(get_jwt_identity())
            user:User = User.query.get(user_id)
            if user is None:
                abort(404, message="User not found.")

            group:Group = Group.query.filter_by(name=data['name'], code=data['code']).first()
            if group is None:
                abort(404, message="Group not found.")

            user_in_group = UserInGroup(group_id=group.id, user_id=user.id)

            db.session.add(user_in_group)
            db.session.commit()

            return jsonify(group.to_dict()), 200
        except ValidationError as e:
            abort(400, message=str(e))
        except IntegrityError as e:
            db.session.rollback()
            abort(409, message=str(e.orig))
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal server error.")