import traceback
from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from db import db
from models.User import User
from schemas import UserPayloadSchema, UserResponseSchema, UserQuerySchema

from flask import request
from sqlalchemy import or_

blp = Blueprint('user', __name__, description='User related CRUD operations.')

@blp.route('/')
class UserCRUD(MethodView):
    """
    User CRUD operations.
    """
    @blp.arguments(UserQuerySchema, location = "query")
    @blp.response(200, UserResponseSchema(many=True))
    @blp.response(500, description="Internal server error.")
    def get(self, data):
        """
        Get all users.
        """
        try:
            username = request.args.get('username')
            email = request.args.get('email')

            filters = []
            if username:
                filters.append(User.username == username)
            if email:
                filters.append(User.email == email)

            if filters:
                users = User.query.filter(or_(*filters)).all()
            else:
                users = User.query.all()

            return jsonify([user.to_dict() for user in users])
        except Exception as e:
            traceback.print_exc()
            abort(500, message="Internal server error.")

    @blp.arguments(UserPayloadSchema)
    @blp.response(201, UserResponseSchema)
    @blp.response(400, description="Bad request.")
    @blp.response(409, description="Conflict.")
    @blp.response(500, description="Internal server error.")
    def post(self, data):
        """
        Register a new user.
        """
        try:
            if User.query.filter_by(username=data['username']).first():
                raise ValidationError("A user with that username already exists.")
            if User.query.filter_by(email=data['email']).first():
                raise ValidationError("A user with that email already exists.")

            unhashed_password = data.get('password', None)
            if not unhashed_password:
                raise ValidationError("Password is required.")
            if not User.validate_password(unhashed_password):
                raise ValidationError("Password must be between 8 and 50 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character from the list: . * _ ? ¿ ! ¡ % # -")

            data['password'] = User.hash_password(unhashed_password)

            user = User(**data)

            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                abort(409, message="A user with that username or email already exists.")

            return jsonify(user.to_dict()), 201
        except ValidationError as e:
            abort(400, message=str(e))
        except Exception as e:
            traceback.print_exc()
            abort(500, message="Internal server error.")