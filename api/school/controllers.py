from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api import db
from api.auth.models import SuperUser
from api.school.models import School, AcademicYear, Class

school = Blueprint("school", __name__, url_prefix="/api/school")

@school.route("/hello")
def school_hello():
    return {"message":"School hello route"}, 200

@school.route("/create", methods=["POST"])
@jwt_required()
def school_create():
    """school_create
    API Data Format:
        name: Name of school to be created
        location: Location of school to be created

    Returns:
        [type]: [description]
    """
    super_user = SuperUser.find_by_public_id(get_jwt_identity())

    if not super_user:
        return {"message":"User is not authorized to create a school"}

    data = request.json

    # Check if school with that name already exists
    school_exists = School.find_by_name(data["name"])

    if school_exists:
        return {"message":"A school with that name already exists"}, 401

    # Create an instance of the school model
    school = School(name=data["name"], location=data["location"])

    db.session.add(school)
    db.session.commit()

    return {"message": f"{data['name']} created successfully"}, 200


@school.route("/modify", methods=["POST"])
@jwt_required()
def school_modify_by_id():
    """school_modify_by_id
    API Data Format:
        id: ID of the current school to be changed
        new_name: Name to be assigned to the current school
        new_location: Location to be assigned to current school
    Returns:
        [type]: [description]
    """
    data = request.json

    # Check if the school exists
    school_exists = School.find_by_id(data["id"])
    if not school_exists:
        return {"message": "A school with the given ID does not exist"}, 401

    # Check if a school with the new name exists
    school_with_new_name_exists = School.find_by_name(data["new_name"])
    if school_with_new_name_exists:
        return {"message": "A school with that name already exists"}, 401

    school = School.find_by_id(data["id"])

    if data["new_name"]:
        school.name = data["new_name"]
    if data["new_location"]:
        school.locatioon = data["new_location"]

    return {"message": "School updated successfully"}, 200

@school.route("/delete",methods=["POST"])
@jwt_required()
def school_delete_by_id():
    """school_delete_by_id

    API Data Format:
        id: ID of school to be deleted
    Returns:
        [type]: [description]
    """
    data = request.json

    # Check if the school exists
    school_exists = School.find_by_id(data["id"])
    if not school_exists:
        return {"message": "A school with the given ID does not exist"}, 401

    # Delete school
    db.session.delete(school_exists)
    db.session.commit()

    return {"message": "School deleted successfully"}, 200
