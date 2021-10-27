from api.fees.models import Fees
from flask import Blueprint

fees = Blueprint("fees", __name__, url_prefix="/api/fees")


@fees.route("/hello")
def fees_hello():
    return {"message": "Fees blueprint working"}


# TODO: Add new payment [Admin]
# TODO: Modify existing payment [SuperUser / Owner]
# TODO: Delete payment [SuperUser / Owner]
