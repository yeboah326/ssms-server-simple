from flask import Blueprint
from api.expenditure.models import Expenditure

expenditure = Blueprint("expenditure", __name__, url_prefix="/api/expenditure")


@expenditure.route("/hello", methods=["GET"])
def hello():
    return {"message": "Expenditure blueprint working"}, 200
