from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api import db
from api.student.models import Student
from api.school.models import Class
from api.auth.utils import current_user_type

student = Blueprint("student", __name__, url_prefix="/api/student")


@student.route("/hello", methods=["GET"])
def student_hello():
    return {"message": "Student blueprint working"}, 200


# TODO: Create new student [Admin]
@student.route("/class/<class_id>", methods=["POST"])
@jwt_required()
def student_create_new(class_id):
    """student_create_new

    Args:
        class_id (Intger): The ID of the class the student belongs to

    API Data Format:
        name (String): Name of the student
        date_of_birth (Date,Optional): Date of birth of the student

    Returns:
        response_body (dict): [description]
        status_code (Integer): HTTP status code of reponse
    """
    # Check if user is a super_user, admin, owner
    if not current_user_type(get_jwt_identity(), ["super_user", "admin", "owner"]):
        return {
            "message": "User does not have the right priveleges to perform specified actions"
        }, 401

    data = request.get_json()

    # Two instances for when the date of birth is provided or not provided
    try:
        student = Student(
            name=data["name"],
            date_of_birth=data["date_of_birth"],
            class_id=class_id,
            scholarship=data["scholarship"],
        )
    except KeyError:
        student = Student(name=data["name"], class_id=class_id)

    db.session.add(student)
    db.session.commit()

    return {"message": "Student created successfully"}, 200


# TODO: Modify student [SuperUser / Owner]
@student.route("/<student_id>", methods=["PUT"])
@jwt_required()
def student_modify_by_id(student_id):
    """student_modify_by_id

    Args:
        student_id (Intger): The ID of the student to be modified

    API Data Format:
        new_name (String): Name of the student
        new_date_of_birth (Date,Optional): Date of birth of the student

    Returns:
        response_body (dict): [description]
        status_code (Integer): HTTP status code of reponse
    """
    # Check if user is a super_user, admin, owner
    if not current_user_type(get_jwt_identity(), ["super_user", "admin", "owner"]):
        return {
            "message": "User does not have the right priveleges to perform specified actions"
        }, 401

    data = request.get_json()

    student = Student.find_by_id(id=student_id)

    # Check if student exists
    if not student:
        return {"message": "Student does not exist"}, 404

    try:
        if data["new_name"]:
            student.name = data["new_name"]

        if data["new_date_of_birth"]:
            student.date_of_birth = data["new_date_of_birth"]
        
        if data["new_scholarship"]:
            student.scholarship = data["new_scholarship"]
    except KeyError:
        pass
    db.session.commit()

    return {"message": "Student updated successfully"}, 200


# TODO: Delete student [SuperUser / Owner]
@student.route("/<student_id>", methods=["DELETE"])
@jwt_required()
def student_delete_by_id(student_id):
    """student_delete_by_id

    Args:
        student_id (Intger): The ID of the student to be modified

    Returns:
        response_body (dict): [description]
        status_code (Integer): HTTP status code of reponse
    """
    # Check if user is a super_user, admin, owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {"message": "User is not authorized to delete student"}, 401

    student = Student.find_by_id(id=student_id)

    # Check if student exists
    if not student:
        return {"message": "Student does not exist"}, 404

    db.session.delete(student)
    db.session.commit()

    return {"message": "Student deleted successfully"}, 200


@student.route("/class/<class_id>", methods=["GET"])
@jwt_required()
def student_get_all_by_class_id(class_id):
    """student_get_all_by_class_id

    Args:
        class_id (Intger): The ID of the class whose student are to be retrieved

    Returns:
        response_body (dict): [description]
        status_code (Integer): HTTP status code of reponse
    """
    # Check if user is a super_user, admin, owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner", "admin"]):
        return {"message": "User is not authorized to get all students in a class"}, 401

    school_class_students = Class.find_by_id(class_id).students

    return {"students": school_class_students}, 200


@student.route("/class/<class_id>/search", methods=["GET"])
@jwt_required()
def student_search_by_name(class_id):
    SEARCH_NAME = request.args.get("name")

    # Check if user is a super_user, admin, owner
    if not current_user_type(get_jwt_identity(), ["super_user", "owner", "admin"]):
        return {"message": "User is not authorized to perform this search"}, 401

    school_class_students = Student.query.filter(
        Student.name.ilike(f"%{SEARCH_NAME}%"), Student.class_id == class_id
    ).all()

    return {"students": school_class_students}, 200
