from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from api import db
from api.auth.models import User

auth = Blueprint("auth", __name__,url_prefix="/api/auth")

@auth.route("/hello")
def hello():
    return {"message":"Auth blueprint is working"}, 200

@auth.route("/token", methods=["POST"])
def create_token():
    data = request.json

    # Checks whether a user with the given username exists
    user = User.find_by_username(data["username"])
    if user:
        password_correct = user.check_password(data["password"])
        if password_correct:
            access_token = create_access_token(identity=user.public_id)
            return {"token":access_token, "user_id":user.public_id}, 200
        return {"message": "Invalid credentials"}, 401

@auth.route("/protected")
@jwt_required()
def protected():
    return {"message": "Protected route"}