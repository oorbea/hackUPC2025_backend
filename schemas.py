import json
from marshmallow import INCLUDE, Schema, ValidationError, fields, pre_load

class UserPayloadSchema(Schema):
    """
    Schema for user payload.
    """
    username = fields.Str(required=True, error_messages={"required": "Username is required."}, metadata={"description": "Username of the user."})
    email = fields.Email(required=True, error_messages={"required": "Email is required."}, metadata={"description": "Email of the user."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."}, metadata={"description": "Password of the user."})

class UserResponseSchema(Schema):
    """
    Schema for user response.
    """
    id = fields.Int(required=True, metadata={"description": "ID of the user."})
    username = fields.Str(required=True, metadata={"description": "Username of the user."})
    email = fields.Email(required=True, metadata={"description": "Email of the user."})
    picture = fields.Str(metadata={"description": "Profile picture filename of the user."})
    created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S', metadata={"description": "Creation date of the user."})