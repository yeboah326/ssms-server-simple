from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from api import db
from api.auth.models import User

auth = Blueprint("auth", __name__,url_prefix="/api/auth")

@auth.route("/hello")
def hello():
    return {"message":"Auth blueprint is working"}, 200

@auth.route("/token", methods=["POST"])
def auth_create_new_token():
    data = request.json

    # Checks whether a user with the given username exists
    user = User.find_by_username(data["username"])
    if user:
        password_correct = user.check_password(data["password"])
        if password_correct:
            access_token = create_access_token(identity=user.public_id)
            return {"token":access_token, "user_id":user.public_id}, 200
        return {"message": "Invalid credentials"}, 401

@auth.route("/register", methods=["POST"])
def create_new_user_account():
    data = request.json

    user_type = data["user_type"]

    email_exists = User.find_by_email(data["email"])

    if email_exists:
        return {"message": "A user with this email already exists"}, 401

    user = User(username=data["username"],name=data["name"],email=data["email"])
    user.password = data["password"]

    # Assign the user type to the temporary instance created
    if user_type == "admin":
        user.is_admin = True
    elif user_type == "super_user":
        user.is_super_user = True
    elif user_type == "auditor":
        user.is_auditor = True

    db.session.add(user)
    db.session.commit()

    return {"message": "User created successfully", "user": User.find_by_email(data)}, 200

@auth.route("/protected")
@jwt_required()
def protected():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(user.name)
    return {"message": "Protected route", "users": user_list}