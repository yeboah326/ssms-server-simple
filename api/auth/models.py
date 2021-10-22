from uuid import uuid4
from api import db
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    """User Model

    Args:
        db ([type]): [description]
    """
    __tablename__ = "ssms_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    username =db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))

    def __repr__(self) -> str:
        return (
            f"<User {self.email}, public_id={self.public_id}, is_admin={self.is_admin}, is_auditor={self.is_auditor}>"
        )

    @property
    def password(self):
        raise AttributeError("password: write-only field")
    
    @password.setter
    def password(self, password) -> None:
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()
    
    @classmethod
    def check_user_credentials(cls, username, password):
        return cls.query.filter_by(username=username,password=password)

class SuperUser(User):
    __tablename__ = "ssms_superuser"
    id = db.Column(db.Integer, db.ForeignKey("ssms_user.id") ,primary_key=True, autoincrement=True)
    is_super_user = db.Column(db.Boolean, default=True)

class SchoolUser(User):
    __tablename__ = "ssms_schooluser"
    id = db.Column(db.Integer, db.ForeignKey("ssms_user.id") ,primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, db.ForeignKey('ssms_school.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_auditor = db.Column(db.Boolean, default=False)
    is_teacher = db.Column(db.Boolean, default=False)
