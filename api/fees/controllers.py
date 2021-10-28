from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api import db
from api.student.models import Student
from api.fees.models import Fees
from api.auth.utils import current_user_type

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

    fees = Student.find_by_id(student_id).fees

    return {"expenditures": fees}, 200
