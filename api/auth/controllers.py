from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_current_user
from flask_jwt_extended.utils import get_jwt
from api import db
from api.auth.models import SchoolUser, SuperUser, User

auth = Blueprint("auth", __name__,url_prefix="/api/auth")

@auth.route("/hello", methods=["GET"])
def hello():
    return {"message":"Auth blueprint is working"}, 200

@auth.route("/token", methods=["POST"])
def auth_create_new_token():
    """auth_create_new_token
    API Data Format:
        username: Username of the user trying to login
        password: Password of the user trying to login
    Returns:
        [type]: [description]
    """
    data = request.json

    # Checks whether a user with the given username exists
    user = User.find_by_username(data["username"])
    if user:
        password_correct = user.check_password(data["password"])
        if password_correct:
            access_token = create_access_token(identity=user.public_id)
            return {"token":access_token, "user_id":user.public_id}, 200
        return {"message": "Username or password is invalid"}, 401

@auth.route("/register", methods=["POST"])
def auth_create_new_user_account():
    data = request.json

    user_type = data["user_type"]

    email_exists = User.find_by_email(data["email"])

    if email_exists:
        return {"message": "A user with this email already exists"}, 401


    # Assign the user type to the temporary instance created
    if user_type == "super_user":
        super_user = SuperUser(username=data["username"],name=data["name"],email=data["email"])
        super_user.password = data["password"]
        db.session.add(super_user)
        db.session.commit()
    elif user_type == "admin":
        school_user = SchoolUser(username=data["username"],name=data["name"],email=data["email"], is_admin=True, school_id=data["school_id"])
        school_user.password = data["password"]
        db.session.add(school_user)
        db.session.commit()
    elif user_type == "auditor":
        school_user = SchoolUser(username=data["username"],name=data["name"],email=data["email"], is_auditor=True, school_id=data["school_id"])
        school_user.password = data["password"]
        db.session.add(school_user)
        db.session.commit()
    elif user_type == "teacher":
        school_user = SchoolUser(username=data["username"],name=data["name"],email=data["email"], is_teacher=True, school_id=data["school_id"])
        school_user.password = data["password"]
        db.session.add(school_user)
        db.session.commit()

    return {"message": "User created successfully", "user": User.find_by_email(data["email"]).name}, 200

@auth.route("/protected")
@jwt_required()
def protected():
    # su = SuperUser.query.filter_by(id=User.query.filter_by(public_id))
    
    su = SuperUser.query.filter_by(id=User.query.filter_by(public_id=get_jwt_identity()).first().id)
    if not su:
        return {"message":"User does not have the right priveleges to perform specified actions"}
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(user.name)
    return {"message": "Protected route", "users": user_list}