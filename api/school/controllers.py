from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from api import db
from api.school.models import School

school = Blueprint("school", __name__, url_prefix="/api/school")

@school.route("/hello")
def school_hello():
    return {"message":"School hello route"}, 200

@school.route("/create", methods=["POST"])
def school_create():
    """school_create
    API Data Format:
        name: Name of school to be created
        location: Location of school to be created

    Returns:
        [type]: [description]
    """
    data = request.json

    # Check if school with that name already exists
    school_exists = School.find_by_name(data["name"]).first()

    if school_exists:
        return {"message":"A school with that name already exists"}, 401
    
    # Create an instance of the school model
    school = School(name=data["name"], location=data["location"])

    db.session.add(school)
    db.session.commit()

    return {"message": f"{data['name']} created succesfully"}, 200


@school.route("/modify/", methods=["POST"])
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
        return {"message": "A school with the given ID does not exit"}, 401
    
    # Check if a school with the new name exists
    school_with_new_name_exists = School.find_by_name(data["new_name"])
    if school_with_new_name_exists:
        return {"message": "A school with that name already exists"}, 401
    
    school = School.find_by_id(data["id"])

    if data["new_name"]:
        school.name = data["new_name"]
    if data["new_location"]:
        school.locatioon = data["location"]
    
    return {"message": "School updated successfully"}, 200

@school.route("/delete/<school_id>")
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
    School.find_by_id(data["id"]).delete()
    db.session.commit()

    return {"message": "School deleted successfully"}, 200