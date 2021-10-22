from flask import Blueprint
from flask_jwt_extended import jwt_required
from api.school.models import School

school = Blueprint("school", __name__, url_prefix="/api/school")

@school.route("/hello")
def school_hello():
    return {"message":"School hello route"}

#TODO: Create school
@school.route("/create/<school_id>")
def school_create_by_id():
    pass


#TODO: Modifiy school
@school.route("/modify/<school_id>")
def school_modify_by_id():
    pass

#TODO: Delete school
@school.route("/delete/<school_id>")
def delete_school_by_id():
    pass