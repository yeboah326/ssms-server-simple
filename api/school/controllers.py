from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api import db
from api.auth.utils import current_user_type
from api.auth.models import SuperUser, SchoolUser, User
from api.school.models import School, AcademicYear, Class

school = Blueprint("school", __name__, url_prefix="/api/school")


@school.route("/hello")
def school_hello():
    return {"message": "School hello route"}, 200


# -------------------------------------------------------

# ---------------------------------#
# ENDPOINT: School                #
# ---------------------------------#
@school.route("/create", methods=["POST"])
@jwt_required()
def school_create():
    """school_create

    API Data Format:
        name: Name of school to be created
        location: Location of school to be created

    Returns:
        dict: Response body
        Integer: Status Code
    """

    if not current_user_type(get_jwt_identity(), ["super_user"]):
        return {"message": "User is not authorized to create a school"}

    data = request.json

    # Check if school with that name already exists
    school_exists = School.find_by_name(data["name"])

    if school_exists:
        return {"message": "A school with that name already exists"}, 401

    # Create an instance of the school model
    school = School(name=data["name"], location=data["location"])

    db.session.add(school)
    db.session.commit()

    return {"message": f"{data['name']} created successfully"}, 200


# TODO: Check the user type before performing the operation
@school.route("/modify", methods=["POST"])
@jwt_required()
def school_modify_by_id():
    """school_modify_by_id

    API Data Format:
        id: ID of the current school to be changed
        new_name: Name to be assigned to the current school
        new_location: Location to be assigned to current school

    Returns:
        dict: Response body
        Integer: Status Code
    """
    data = request.json

    # Check if the school exists
    school_exists = School.find_by_id(data["id"])
    if not school_exists:
        return {"message": "A school with the given ID does not exist"}, 404

    # Check if a school with the new name exists
    school_with_new_name_exists = School.find_by_name(data["new_name"])
    if school_with_new_name_exists:
        return {"message": "A school with that name already exists"}, 401

    school = School.find_by_id(data["id"])

    if data["new_name"]:
        school.name = data["new_name"]
    if data["new_location"]:
        school.locatioon = data["new_location"]

    db.session.commit()

    return {"message": "School updated successfully"}, 200


@school.route("/delete", methods=["POST"])
@jwt_required()
def school_delete_by_id():
    """school_delete_by_id

    API Data Format:
        id: ID of school to be deleted

    Returns:
        dict: Response body
        Integer: Status Code
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


# -------------------------------------------------------

# ---------------------------------#
# ENDPOINT: Academic Year         #
# ---------------------------------#
@school.route("/academic_year", methods=["POST"])
@jwt_required()
def school_create_academic_year():
    """school_create_academic_year

    API Data Format:
        name: String
        school_id: Integer

    Returns:
        dict: Response body
        Integer: Status Code
    """
    data = request.json

    # Check whether user is super_user or owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {
            "message": "User does not have the right priveleges to perform specified actions"
        }, 401

    # Creating new instance of academic year
    academic_year = AcademicYear(name=data["name"], school_id=data["school_id"])

    # Saving the created instance
    db.session.add(academic_year)
    db.session.commit()

    return {"message": "Academic year created successfully"}, 200


@school.route("/academic_year", methods=["DELETE"])
@jwt_required()
def school_delete_academic_year():
    """school_delete_academic_year

    API Data Format:
        academic_year_id: Integer

    Returns:
        dict: Response body
        Integer: Status Code
    """
    data = request.json

    # Check whether user is super_user or owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {
            "message": "User does not have the right priveleges to perform specified actions"
        }, 401

    # Find the academic year
    academic_year = AcademicYear.find_by_id(academic_year_id=data["academic_year_id"])

    # Error message if the academic year does not exist
    if not academic_year:
        return {"message": "Academic does not exist"}, 404

    # Delete academic year
    db.session.delete(academic_year)
    db.session.commit()

    return {"message": "Academic year deleted successfully"}, 200


@school.route("/academic_year", methods=["PUT"])
@jwt_required()
def school_modify_academic_year():
    """school_modify_academic_year

    API Data Format:
        academic_year_id: Integer
        new_academic_year_name: String

    Returns:
        dict: Response body
        Integer: Status Code
    """
    data = request.json

    # Check whether user is super_user or owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {
            "message": "User does not have the right priveleges to perform specified actions"
        }, 401

    # Find the academic year
    academic_year = AcademicYear.find_by_id(academic_year_id=data["academic_year_id"])

    # Error message if the academic year does not exist
    if not academic_year:
        return {"message": "Academic year does not exist"}, 404

    academic_year.name = data["new_academic_year_name"]
    db.session.commit()

    return {"message": "Academic year updated successfully"}, 200


@school.route("/academic_year", methods=["GET"])
@jwt_required()
def school_get_all_academic_years():
    # Retrieve the logged in user
    school_user = SchoolUser.find_by_public_id(public_id=get_jwt_identity())

    # Retrieve the academic years of the logged in user
    academic_years = School.find_by_id(id=school_user.school_id).academic_years

    academic_years_json = {}

    for academic_year in academic_years:
        academic_years_json[academic_year.id] = academic_year.name

    return {"academic_years": academic_years_json}, 200


# -------------------------------------------------------

# ---------------------------------#
# ENDPOINT: Class                 #
# ---------------------------------#
@school.route("/class", methods=["POST"])
@jwt_required()
def school_create_class():
    """school_create_class

    API Data Format:
        academic_year_id: Integer
        class_name: String

    Returns:
        dict: Response body
        Integer: Status Code
    """
    data = request.json

    # Check whether user is super_user or owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {
            "message": "User does not have the right priveleges to perform specified actions"
        }, 401

    # Create new instance of school class
    school_class = Class(
        name=data["class_name"], academic_year_id=data["academic_year_id"]
    )

    db.session.add(school_class)
    db.session.commit()

    return {"message": "Class created successfully"}, 200


@school.route("/class", methods=["DELETE"])
@jwt_required()
def school_delete_class():
    """school_delete_class

    API Data Format:
        class_id: Integer

    Returns:
        dict: Response body
        Integer: Status Code
    """
    data = request.json

    # Check whether user is super_user or owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {
            "message": "User does not have the right priveleges to perform specified actions"
        }, 401

    # Find the existing class model
    school_class = Class.find_by_id(id=data["class_id"])

    if not school_class:
        return {"message": "Class does not exist"}, 404

    db.session.delete(school_class)
    db.session.commit()

    return {"message": "Class deleted successfully"}, 200


@school.route("/class", methods=["PUT"])
@jwt_required()
def school_modify_class():
    """school_modify_class

    API Data Format:
        class_id: Integer
        new_class_name: String

    Returns:
        dict: Response body
        Integer: Status Code
    """
    data = request.json

    # Check whether user is super_user or owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {
            "message": "User does not have the right priveleges to perform specified actions"
        }, 401

    # Find the existing class model
    school_class = Class.find_by_id(id=data["class_id"])

    if not school_class:
        return {"message": "Class does not exist"}, 404

    if data["new_class_name"]:
        school_class.name = data["new_class_name"]

    db.session.commit()

    return {"message": "Class modified successfully"}, 200


@school.route("academic_year/<academic_year_id>/class", methods=["GET"])
@jwt_required()
def school_get_all_class(academic_year_id):

    academic_year = AcademicYear.find_by_id(academic_year_id)

    if not academic_year:
        return {"message": "Academic year not found"}, 404

    classes = academic_year.classes

    classes_json = {}

    for school_class in classes:
        classes_json[school_class.id] = school_class.name

    return {"academic_year": academic_year.name, "classes": classes_json}, 200


# -------------------------------------------------------
