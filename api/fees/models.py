from dataclasses import dataclass
from api import db


@dataclass
class Fees(db.Model):
    id: int
    student_id: int
    amount: float

    __tablename__ = "ssms_fees"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("ssms_student.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    @classmethod
    def find_by_fee_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
