import json
import os
from random import randint
import traceback
from flask import current_app, jsonify, request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from db import db
from models.User import User
from schemas import TokenResponseSchema, UserLoginSchema, UserPayloadSchema, UserProfilePictureSchema, UserResponseSchema
from globals import ALLOWED_PICTURE_EXTENSIONS, PROFILE_PICTURES_DIR
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

blp = Blueprint('user', __name__, description='User related CRUD operations.')

def allowed_file(filename: str) -> bool:
    """
    Check if the profile picture is allowed based on its extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PICTURE_EXTENSIONS

@blp.route('/')
class UserCRUD(MethodView):
    """
    User CRUD operations.
    """
    @blp.response(200, UserResponseSchema(many=True))
    @blp.response(500, description="Internal server error.")
    def get(self):
        """
        Get all users.
        """
        try:
            users:list[User] = User.query.all()
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

@blp.route('/login')
class UserLogin(MethodView):
    """
    User login to obtain a JWT.
    """
    @blp.arguments(UserLoginSchema)
    @blp.response(200, TokenResponseSchema)
    @blp.response(400, description="Bad request.")
    @blp.response(401, description="Unauthorized.")
    @blp.response(500, description="Internal server error.")
    def post(self, login_data):
        """
        login a user and return a JWT token.
        """
        try:
            user:User = User.query.filter_by(username=login_data['username']).first()
            if not user:
                abort(401, message="Invalid username or password.")

            if not user.verify_hashed_password(login_data['password']):
                abort(401, message="Invalid username or password.")

            access_token = create_access_token(identity=user.id)

            return jsonify({"token": access_token})

        except ValidationError as ve:
            abort(400, message=ve.messages)
        except Exception:
            traceback.print_exc()
            abort(500, message="Internal server error.")


@blp.route('/profile_picture')
class UserProfilePicture(MethodView):
    """
    Upload or update the authenticated user's profile picture.
    """
    @jwt_required()
    @blp.arguments(UserProfilePictureSchema, location='form')
    @blp.response(200, UserResponseSchema)
    @blp.response(400, description="Bad request.")
    @blp.response(401, description="Unauthorized.")
    @blp.response(404, description="User not found.")
    @blp.response(500, description="Internal server error.")
    @blp.doc(security=[{"jwt": []}])
    def patch(self, form_data):
        """
        Accepts multipart/form-data:
          - picture: required file (png, jpg, jpeg, gif)

        Returns the updated User object.
        """
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                abort(404, message="User not found.")

            picture = form_data.get('picture')
            if not picture:
                abort(400, message="Missing 'picture' file.")

            original_filename = picture.filename or ""
            filename = secure_filename(
                f"{user_id}_{randint(1000,9999)}_{original_filename}"
            )
            if not allowed_file(filename):
                abort(
                    400,
                    message=(
                        "Invalid file type. "
                        f"Allowed types: {', '.join(ALLOWED_PICTURE_EXTENSIONS)}"
                    )
                )

            upload_dir = PROFILE_PICTURES_DIR
            os.makedirs(upload_dir, exist_ok=True)

            save_path = os.path.join(upload_dir, filename)
            picture.save(save_path)

            user.picture = filename
            db.session.commit()

            return jsonify(user.to_dict())

        except ValidationError as ve:
            abort(400, message=str(ve))
        except IntegrityError:
            db.session.rollback()
            abort(500, message="Database integrity error.")
        except Exception:
            traceback.print_exc()
            abort(500, message="Internal server error.")
    