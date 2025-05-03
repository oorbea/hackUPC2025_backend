import re
from sqlalchemy import func
from db import db
from schemas import UserResponseSchema

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)
    picture = db.Column(db.String(200), nullable=True)
    reset_code = db.Column(db.Integer(), nullable=True)
    reset_code_expiration = db.Column(db.DateTime(), nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"
    
    def to_dict(self) -> UserResponseSchema:
        """
        Convert the User object to a dictionary.
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'picture': self.picture,
            'created_at': self.created_at.strftime('iso')
        }
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash the password using a secure hashing algorithm.
        """
        from werkzeug.security import generate_password_hash
        return generate_password_hash(password)
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate that the password is secure enough.
        """
        password_re = re.compile(
            r'^(?=.{8,50}$)'        # longitud entre 8 y 50
            r'(?=.*[a-z])'          # al menos una minúscula
            r'(?=.*[A-Z])'          # al menos una mayúscula
            r'(?=.*\d)'             # al menos un dígito
            r'(?=.*[.\*_?¿!¡%#-])'  # al menos un carácter especial de la lista
            r'.*$'
        )

        return bool(password_re.match(password))
    
    def verify_hashed_password(self, password: str) -> bool:
        """
        Verify the hashed password.
        """
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)