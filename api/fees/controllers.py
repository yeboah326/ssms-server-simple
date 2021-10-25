from api.fees.models import Fees
from flask import Blueprint

fees = Blueprint("fees", __name__ , url_prefix="/api/fees")

@fees.route("/hello")
def fees_hello():
    return {"message":"Fees blueprint working"}
