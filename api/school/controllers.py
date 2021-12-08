from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api import db
from api.auth.utils import current_user_type
from api.auth.models import SuperUser, SchoolUser, User
from api.school.models import School, AcademicYear, Class
from api.fees.models import FeesToBePaid

school = Blueprint("school", __name__, url_prefix="/api/school")


@school.route("/hello", methods=["GET"])
def school_hello():
    return {"message": "School hello route"}, 200


# -------------------------------------------------------

# ---------------------------------#
# ENDPOINT: School                #
# ---------------------------------#
@school.route("", methods=["POST"])
@jwt_required()
def school_create():
    """school_create

    Authorized User:
        super_user

    API Data Format:
        name: Name of school to be created
        location: Location of school to be created

    Returns:
        dict: Response body
        Integer: Status Code
    """

    if not current_user_type(get_jwt_identity(), ["super_user"]):
        return {"message": "User is not authorized to create a school"}, 401

    data = request.json

    # Check if school with that name already exists
    school_exists = School.find_by_name(data["name"])

    if school_exists:
        return {"message": "A school with that name already exists"}, 400

    # Create an instance of the school model
    school = School(name=data["name"], location=data["location"])

    db.session.add(school)
    db.session.commit()

    return {"message": f"{data['name']} created successfully"}, 200


# TODO: Check the user type before performing the operation
@school.route("/<school_id>", methods=["PUT"])
@jwt_required()
def school_modify_by_id(school_id):
    """school_modify_by_id

    Authorized User:
        super_user

    API Data Format:
        new_name: Name to be assigned to the current school
        new_location: Location to be assigned to current school

    Returns:
        dict: Response body
        Integer: Status Code
    """

    if not current_user_type(get_jwt_identity(), ["super_user"]):
        return {"message": "User is not authorized to modify school"}, 401

    data = request.json

    # Check if the school exists
    school_exists = School.find_by_id(school_id)
    if not school_exists:
        return {"message": "A school with the given ID does not exist"}, 404

    # Check if a school with the new name exists
    school_with_new_name_exists = School.find_by_name(data["new_name"])
    if school_with_new_name_exists:
        return {"message": "A school with that name already exists"}, 400

    school = School.find_by_id(school_id)

    if data["new_name"]:
        school.name = data["new_name"]
    if data["new_location"]:
        school.location = data["new_location"]

    db.session.commit()

    return {"message": "School updated successfully"}, 200


@school.route("/<school_id>", methods=["DELETE"])
@jwt_required()
def school_delete_by_id(school_id):
    """school_delete_by_id

    Authorized User:
        super_user

    Args:
        id: ID of school to be deleted

    Returns:
        dict: Response body
        Integer: Status Code
    """

    if not current_user_type(get_jwt_identity(), ["super_user"]):
        return {"message": "User is not authorized to delete a school"}, 401

    # Check if the school exists
    school_exists = School.find_by_id(school_id)
    if not school_exists:
        return {"message": "A school with the given ID does not exist"}, 404

    # Delete school
    db.session.delete(school_exists)
    db.session.commit()

    return {"message": "School deleted successfully"}, 200


@school.route("/<school_id>", methods=["GET"])
@jwt_required()
def school_get_by_id(school_id):
    if not current_user_type(
        get_jwt_identity(), ["super_user", "admin", "owner", "teacher", "auditor"]
    ):
        return {"message": "User is not authorized to retrieve a school"}, 401

    school = School.find_by_id(school_id)

    if not school:
        return {"message": "School not found"}, 404

    return {"school": school}, 200


@school.route("/", methods=["GET"])
@jwt_required()
def school_get_all():
    if not current_user_type(get_jwt_identity(), ["super_user"]):
        return {"message": "User is not authorized to retrieve all schools"}, 401

    schools = School.query.all()

    return {"schools": schools}, 200


# -------------------------------------------------------

# ---------------------------------#
# ENDPOINT: Academic Year          #
# ---------------------------------#
@school.route("/academic_year", methods=["POST"])
@jwt_required()
def school_create_academic_year():
    """school_create_academic_year

    Authorized User:
        super_user
        owner

    API Data Format:
        name: String
        school_id: Integer

    Returns:
        dict: Response body
        Integer: Status Code
    """
    # Check whether user is super_user or owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {"message": "User is not authorized to create an academic year"}, 401

    data = request.json

    # Creating new instance of academic year
    academic_year = AcademicYear(name=data["name"], school_id=data["school_id"])

    # Saving the created instance
    db.session.add(academic_year)
    db.session.commit()

    return {"message": "Academic year created successfully"}, 200


@school.route("/academic_year/<academic_year_id>", methods=["DELETE"])
@jwt_required()
def school_delete_academic_year(academic_year_id):
    """school_delete_academic_year

    Authorized User:
        super_user
        owner

    Args:
        academic_year_id: Integer

    Returns:
        dict: Response body
        Integer: Status Code
    """

    # Check whether user is super_user or owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {"message": "User is not authorized to delete academic year"}, 401

    # Find the academic year
    academic_year = AcademicYear.find_by_id(academic_year_id)

    # Error message if the academic year does not exist
    if not academic_year:
        return {"message": "Academic does not exist"}, 404

    # Delete academic year
    db.session.delete(academic_year)
    db.session.commit()

    return {"message": "Academic year deleted successfully"}, 200


@school.route("/academic_year/<academic_year_id>", methods=["PUT"])
@jwt_required()
def school_modify_academic_year(academic_year_id):
    """school_modify_academic_year

    Authorized User:
        super_user
        owner

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
        return {"message": "User is not authorized to modify an academic year"}, 401

    # Find the academic year
    academic_year = AcademicYear.find_by_id(academic_year_id=academic_year_id)

    # Error message if the academic year does not exist
    if not academic_year:
        return {"message": "Academic year does not exist"}, 404

    academic_year.name = data["new_academic_year_name"]
    db.session.commit()

    return {"message": "Academic year updated successfully"}, 200


@school.route("<school_id>/academic_year", methods=["GET"])
@jwt_required()
def school_get_all_academic_years(school_id):
    if not current_user_type(get_jwt_identity(), ["super_user", "owner", "admin"]):
        return {"message": "User is not authorized to retrieve all academic years"}, 401

    # Retrieve the academic years of the logged in user
    academic_years = School.find_by_id(id=school_id).academic_years

    return {"academic_years": academic_years}, 200


# -------------------------------------------------------

# ---------------------------------#
# ENDPOINT: Class                  #
# ---------------------------------#
@school.route("academic_year/<academic_year_id>/class", methods=["POST"])
@jwt_required()
def school_create_class(academic_year_id):
    """school_create_class

    Authorized User:
        super_user
        owner

    API Data Format:
        class_name: String
        fees_to_be_paid: Float

    Returns:
        dict: Response body
        Integer: Status Code
    """
    data = request.json

    # Check whether user is super_user or owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {"message": "User is not authorized to create a class"}, 401

    # Create new instance of school class
    school_class = Class(
        name=data["class_name"],
        academic_year_id=academic_year_id,
    )

    db.session.add(school_class)
    db.session.flush()

    # Create fees instance
    fees_to_be_paid = FeesToBePaid(
        amount=data["fees_to_be_paid"],
        class_id=school_class.id,
        academic_year_id=academic_year_id,
    )

    db.session.add(fees_to_be_paid)
    db.session.commit()

    return {"message": "Class created successfully"}, 200


@school.route("/class/<class_id>", methods=["DELETE"])
@jwt_required()
def school_delete_class(class_id):
    """school_delete_class

    Authorized Users:
        super_user
        owner

    Args:
        class_id: Integer

    Returns:
        dict: Response body
        Integer: Status Code
    """
    data = request.json

    # Check whether user is super_user or owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {"message": "User is not authorized to delete a class"}, 401

    # Find the existing class model
    school_class = Class.find_by_id(id=class_id)

    if not school_class:
        return {"message": "Class does not exist"}, 404

    # Delete all class FeesToBePaid Instances
    # fees_to_be_paid = FeesToBePaid.find_fees_to_be_paid(school_class.academic_year_id, school_class.id).first()
    # db.session.delete(fees_to_be_paid)

    # Delete class instance
    db.session.delete(school_class)
    db.session.commit()

    return {"message": "Class deleted successfully"}, 200


@school.route("/class/<class_id>", methods=["PUT"])
@jwt_required()
def school_modify_class(class_id):
    """school_modify_class

    Authorized Users:
        super_user
        owner

    Args:
        class_id: Integer

    API Data Format:
        new_class_name: String

    Returns:
        dict: Response body
        Integer: Status Code
    """
    data = request.json

    # Check whether user is super_user or owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {"message": "User is not authorized to modify a class"}, 401

    # Find the existing class model
    school_class = Class.find_by_id(id=class_id)

    if not school_class:
        return {"message": "Class does not exist"}, 404

    if data["new_class_name"]:
        school_class.name = data["new_class_name"]

    if data["new_fees"]:
        fees_to_be_paid = FeesToBePaid.find_fees_to_be_paid(
            school_class.academic_year_id, school_class.id
        )
        fees_to_be_paid.amount = data["new_fees"]

    db.session.commit()

    return {"message": "Class modified successfully"}, 200


@school.route("academic_year/<academic_year_id>/class", methods=["GET"])
@jwt_required()
def school_get_all_class(academic_year_id):
    """school_get_all_class

    Authorized Users:
        super_user
        owner
        admin

    Args:
        academic_year_id: Integer


    Returns:
        dict: Response body
        Integer: Status Code
    """
    if not current_user_type(get_jwt_identity(), ["super_user", "owner", "admin"]):
        return {"message": "User is not authorized to retrieve all classes"}, 401

    academic_year = AcademicYear.find_by_id(academic_year_id)

    if not academic_year:
        return {"message": "Academic year not found"}, 404

    classes = academic_year.classes

    return {"academic_year": academic_year.name, "classes": classes}, 200


# -------------------------------------------------------
