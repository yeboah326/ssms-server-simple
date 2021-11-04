from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract, func
from api import db
from api.school.models import AcademicYear
from api.expenditure.models import Expenditure
from api.auth.utils import current_user_type

expenditure = Blueprint("expenditure", __name__, url_prefix="/api/expenditure")


@expenditure.route("/hello", methods=["GET"])
def expenditure_hello():
    return {"message": "Expenditure blueprint working"}, 200


# TODO: Create new expenditure [Admin]
@expenditure.route("/academic_year/<academic_year_id>", methods=["POST"])
@jwt_required()
def expenditure_create_new(academic_year_id):
    """expenditure_create_new

    API Data Format:
        description (String): Summary of what the expenditure is about
        amount (Decimal): How much money the expenditure cost

    Args:
        academic_year_id (Integer): ID for academic year

    Returns:
        dict: Response body
        Integer: Status Code
    """
    if not current_user_type(get_jwt_identity(), ["super_user", "admin", "owner"]):
        return {"message": "User is not authorized to create expenditure"}, 401

    data = request.get_json()

    expenditure = Expenditure(
        description=data["description"],
        amount=data["amount"],
        academic_year_id=academic_year_id,
    )

    db.session.add(expenditure)
    db.session.commit()

    return {"message": "Expenditure created successfully"}, 200


# TODO: Modify expenditure
@expenditure.route("/<expenditure_id>", methods=["PUT"])
@jwt_required()
def expenditure_modify_by_id(expenditure_id):
    """expenditure_modify_by_id

    API Data Format:
        new_description (String): New summary of what the expenditure is about
        new_amount (Decimal): New amount of money the expenditure cost

    Args:
        academic_year_id (Integer): ID for academic year

    Returns:
        dict: Response body
        Integer: Status Code
    """
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {"message": "User is not authorized to modify expenditure"}, 401

    data = request.get_json()

    expenditure = Expenditure.find_by_id(expenditure_id)

    if not expenditure:
        return {"message": "Expenditure not found"}, 404

    if data["new_description"]:
        expenditure.description = data["new_description"]

    if data["new_amount"]:
        expenditure.amount = data["new_amount"]

    db.session.commit()

    return {"message": "Expenditure updated successfully"}, 200


# TODO: Delete expenditure
@expenditure.route("/<expenditure_id>", methods=["DELETE"])
@jwt_required()
def expenditure_delete_by_id(expenditure_id):
    """expenditure_delete_by_id

    Args:
        academic_year_id (Integer): ID for academic year

    Returns:
        dict: Response body
        Integer: Status Code
    """
    if not current_user_type(get_jwt_identity(), ["super_user", "owner"]):
        return {"message": "User is not authorized to delete an expenditure"}, 401

    expenditure = Expenditure.find_by_id(expenditure_id)

    if not expenditure:
        return {"message": "Expenditure not found"}, 404

    db.session.delete(expenditure)
    db.session.commit()

    return {"message": "Expenditure deleted successfully"}, 200


# TODO: Get all expenditure
@expenditure.route("/academic_year/<academic_year_id>", methods=["GET"])
@jwt_required()
def expenditure_get_all_for_academic_year(academic_year_id):
    """expenditure_get_all_for_academic_year

    Query Args:
        page: the current page number for the items
        per_page: the number of items per page
        month: the month of the year

    Args:
        academic_year_id (Integer): ID for academic year

    Returns:
        dict: Response body
        Integer: Status Code
    """
    if not current_user_type(get_jwt_identity(), ["super_user", "admin", "owner"]):
        return {"message": "User is not authorized to retrieve expenditure"}, 401

    PAGE = int(request.args.get("page")) if request.args.get("page") != None else 1
    PER_PAGE = (
        int(request.args.get("per_page")) if request.args.get("per_page") != None else 5
    )
    MONTH = int(request.args.get("month")) if request.args.get("month") != None else 13

    # Query when the month is set to 13 which represents the whole year
    if MONTH == 13:
        expenditures = Expenditure.query.filter_by(
            academic_year_id=academic_year_id
        ).paginate(page=PAGE, per_page=PER_PAGE)

        total_expenditure_sum = db.session.query(
            func.sum(Expenditure.amount).filter(
                Expenditure.academic_year_id == academic_year_id,
            )
        ).all()[0][0]

    else:
        # Query when month has been provided as part of the query parameters
        expenditures = (
            db.session.query(Expenditure)
            .filter(
                extract("month", Expenditure.date_created) == MONTH,
                Expenditure.academic_year_id == academic_year_id,
            )
            .paginate(page=PAGE, per_page=PER_PAGE)
        )

        total_expenditure_sum = db.session.query(
            func.sum(Expenditure.amount).filter(
                extract("month", Expenditure.date_created) == MONTH,
                Expenditure.academic_year_id == academic_year_id,
            )
        ).all()[0][0]

    return {
        "expenditures": expenditures.items,
        "total_expenditure": total_expenditure_sum,
        "total_pages": expenditures.pages,
        "prev_page": expenditures.prev_num,
        "next_page": expenditures.next_num,
    }, 200


@expenditure.route("/<expenditure_id>", methods=["GET"])
@jwt_required()
def expenditure_get_by_id(expenditure_id):
    """expenditure_get_by_id

    Args:
        academic_year_id (Integer): ID for academic year

    Returns:
        dict: Response body
        Integer: Status Code
    """
    if not current_user_type(get_jwt_identity(), ["super_user", "admin", "owner"]):
        return {"message": "User is not authorized to view an expenditure"}, 401

    expenditure = Expenditure.query.filter_by(id=expenditure_id).first()
    if not expenditure:
        return {"message": "Expenditure not found"}, 404

    return {"expenditure": expenditure}, 200
