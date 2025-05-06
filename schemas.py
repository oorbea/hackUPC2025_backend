from marshmallow import Schema, fields

from globals import OPENAI_API_KEY, OPENAI_API_VERSION, OPENAI_ENDPOINT
from helpers.PlacesEnum import PlacesEnum

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
    created_at = fields.DateTime(format='iso', metadata={"description": "Creation date of the user."})

class UserLoginSchema(Schema):
    """
    Schema for user login.
    """
    username = fields.Str(
        required=True,
        metadata={"description": "User's username"}
    )
    password = fields.Str(
        required=True,
        metadata={"description": "User's password in plain text"}
    )

class TokenResponseSchema(Schema):
    """
    Schema for JWT response.
    """
    token = fields.Str(
        required=True,
        metadata={"description": "JWT access token"}
    )

class UserProfilePictureSchema(Schema):
    """
    Schema for user profile picture upload.
    """
    picture = fields.Raw(
        required=True,
        metadata={
            "description": "Image file PNG/JPG/GIF",
            "type": "file"
        }
    )

class UserQuerySchema(Schema):
    """
    Schema for user query.
    """
    username = fields.Str(required=False, metadata={"description": "Username of the user."})
    email = fields.Email(required=False, metadata={"description": "Email of the user."})

class OpenaiSettingsSchema(Schema):
    """
    Schema for OpenAI settings.
    """
    api_key = fields.Str(required=True, metadata={"description": "OpenAI API key."})
    azure_endpoint = fields.Str(required=True, metadata={"description": "OpenAI API base URL."})
    api_version = fields.Str(required=True, metadata={"description": "OpenAI API version."})
    model = fields.Str(required=False, load_default="o4-mini", metadata={"description": "OpenAI model name."})
    temperature = fields.Float(load_default=0.7, metadata={"description": "Text generation temperature"})
    timeout = fields.Int(required=False, load_default=None, metadata={"description": "Timeout in seconds"})
    max_tokens = fields.Int(load_default=None, metadata={"description": "Maximum tokens to generate"})
    stop = fields.List(fields.Str(), load_default=None, metadata={"description": "List of tokens to stop generation"})

class GroupPayloadSchema(Schema):
    """
    Schema for group payload.
    """
    name = fields.Str(required=True, error_messages={"required": "Group name is required."}, metadata={"description": "Name of the group."})
    description = fields.Str(required=False, allow_none=True, metadata={"description": "Description of the group."})
    deadline = fields.DateTime(format='iso', required=True, error_messages={"required": "Group deadline is required."}, metadata={"description": "Deadline of the group."})

class GroupResponseSchema(Schema):
    """
    Schema for group response.
    """
    id = fields.Int(required=True, metadata={"description": "ID of the group."})
    name = fields.Str(required=True, metadata={"description": "Name of the group."})
    description = fields.Str(allow_none=True, metadata={"description": "Description of the group."})
    code = fields.Int(required=True, metadata={"description": "Code of the group."})
    deadline = fields.DateTime(format='iso', required=True, metadata={"description": "Deadline of the group."})
    response = fields.Str(allow_none=True, metadata={"description": "AI response of the group."})
    created_at = fields.DateTime(format='iso', required=True, metadata={"description": "Creation date of the group."})

class EnterGroupSchema(Schema):
    """
    Schema for entering a group using a code.
    """
    name = fields.Str(required=True, error_messages={"required": "Group name is required."}, metadata={"description": "Name of the group."})
    code = fields.Int(required=True, error_messages={"required": "Group code is required."}, metadata={"description": "Code of the group."})

class DemandPayloadSchema(Schema):
    """
    Schema for demand payload.
    """
    group_id = fields.Int(required=True, error_messages={"required": "Group ID is required."}, metadata={"description": "ID of the group."})
    places = fields.List(fields.Str(validate=lambda x: x in PlacesEnum.get_members()), required=True, error_messages={"required": "Places are required."}, metadata={"description": "List of places. Valid values are: " + ", ".join(PlacesEnum.get_members())})
    price = fields.Int(required=True, error_messages={"required": "Price is required."}, metadata={"description": "Maximum price."})
    description = fields.Str(required=True, error_messages={"required": "Description is required."}, metadata={"description": "Description of the demand."})

class DemandResponseSchema(Schema):
    """
    Schema for demand response.
    """
    group_id = fields.Int(required=True, metadata={"description": "ID of the group."})
    user_id = fields.Int(required=True, metadata={"description": "ID of the user."})
    places = fields.List(fields.Str(validate=lambda x: x in PlacesEnum.get_members()), required=True, metadata={"description": "List of places. Valid values are: " + ", ".join(PlacesEnum.get_members())})
    price = fields.Int(required=True, metadata={"description": "Maximum price."})
    description = fields.Str(required=True, metadata={"description": "Description of the demand."})
    created_at = fields.DateTime(format='iso', required=True, metadata={"description": "Creation date of the demand."})