from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from api import db
from api.student.models import Student
from api.fees.models import Fees
from api.school.models import Class
from api.auth.utils import current_user_type
from api.student.utils import check_student_paid_fees_in_full

fees = Blueprint("fees", __name__, url_prefix="/api/fees")


@fees.route("/hello", methods=["GET"])
def fees_hello():
    return {"message": "Fees blueprint working"}, 200


# TODO: Add new payment [Admin]
@fees.route("/student/<student_id>", methods=["POST"])
@jwt_required()
def fees_create_new_payment(student_id):
    """fees_create_new_payment

    Authorized User:
        super_user
        admin
        owner

    API Data Format:
        amount (Float): Amount in fees paid by the student

    Args:
        student_id (Integer): ID of student who is paying the fees

    Returns:
        dict: Response body
        Integer: Status Code
    """

    if not current_user_type(get_jwt_identity(), ["super_user", "admin", "owner"]):
        return {"message": "User is not authorized to create fee payment"}, 401

    data = request.get_json()

    fee = Fees(student_id=student_id, amount=data["amount"])

    db.session.add(fee)
    db.session.commit()

    # Check whether student has paid fees in full
    student = Student.find_by_id(student_id)
    student.fees_paid_in_full = check_student_paid_fees_in_full(student_id)[
        "paid_in_full"
    ]
    db.session.commit()

    return {"message": "Fee payment created successfully"}, 200


# TODO: Modify existing payment [SuperUser / Owner]
@fees.route("/<fee_id>", methods=["PUT"])
@jwt_required()
def fees_modify_payment_by_id(fee_id):
    """fees_modify_payment_by_id

    Authorized User:
        super_user
        owner

    API Data Format:
        new_amount (Float): New payment amount to be made

    Args:
        fee_id (Integer): ID of fee to be modified

    Returns:
        dict: Response body
        Integer: Status Code
    """
    data = request.get_json()

    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {"message": "User is not authorized to modify fee payment"}, 401

    fee = Fees.find_by_fee_by_id(fee_id)

    if not fee:
        return {"message": "Fee payment not found"}, 404

    if data["new_amount"]:
        fee.amount = data["new_amount"]

    db.session.commit()

    # Check whether student has paid fees in full
    student = Student.find_by_id(fee.student_id)
    student.fees_paid_in_full = check_student_paid_fees_in_full(fee.student_id)[
        "paid_in_full"
    ]
    db.session.commit()

    return {"message": "Fee payment updated successfully"}, 200


# TODO: Delete payment [SuperUser / Owner]
@fees.route("/<fee_id>", methods=["DELETE"])
@jwt_required()
def fees_delete_payment_by_id(fee_id):
    """fees_delete_payment_by_id

    Authorized User:
        super_user
        owner

    Args:
        fee_id (Integer): ID of fee to be modified

    Returns:
        dict: Response body
        Integer: Status Code
    """
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {"message": "User is not authorized to delete fee payment"}, 401

    fee = Fees.find_by_fee_by_id(fee_id)

    if not fee:
        return {"message": "Fee payment not found"}, 404

    db.session.delete(fee)
    db.session.commit()

    # Check whether student has paid fees in full
    student = Student.find_by_id(fee.student_id)
    student.fees_paid_in_full = check_student_paid_fees_in_full(fee.student_id)[
        "paid_in_full"
    ]
    db.session.commit()

    return {"message": "Fee payment deleted successfully"}, 200


# TODO: Get all fee payments
@fees.route("/student/<student_id>", methods=["GET"])
@jwt_required()
def fees_get_all_student_fee_payments(student_id):
    """fees_get_all_student_fee_payments

    Authorized User:
        super_user
        admin
        owner

    Args:
        student_id (Integer): ID for student

    Returns:
        dict: Response body
        Integer: Status Code
    """
    if not current_user_type(get_jwt_identity(), ["super_user", "admin", "owner"]):
        return {
            "message": "User is not authorized to retrieve student fee payment"
        }, 401

    student = Student.find_by_id(student_id)

    student_info = check_student_paid_fees_in_full(student_id)

    return {
        "fees": student.fees,
        "student": student,
        "total_amount_paid": student_info["fees_paid"],
        "total_amount_to_be_paid": student_info["fees_to_be_paid"],
    }, 200


# TODO: Get all fee payments for class
@fees.route("/students/<class_id>", methods=["GET"])
@jwt_required()
def fees_get_all_students_fee_payments(class_id):
    if not current_user_type(get_jwt_identity(), ["super_user", "admin", "owner"]):
        return {
            "message": "User is not authorized to retrieve student fee payment"
        }, 401

    school_class = Class.find_by_id(class_id)

    class_students = school_class.students

    if len(class_students) == 0:
        return {"message": "There are no students in class"}
    return {"students": class_students}
