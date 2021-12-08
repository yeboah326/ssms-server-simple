from dataclasses import dataclass
from api import db


@dataclass
class Fees(db.Model):
    id: int
    student_id: int
    amount: float

    __tablename__ = "ssms_fees"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("ssms_student.id", ondelete="cascade"), nullable=False
    )
    amount = db.Column(db.Float, nullable=False)

    @classmethod
    def find_by_fee_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


@dataclass
class FeesToBePaid(db.Model):
    id: int
    amount: float
    class_id: int
    academic_year_id: int

    __tablename__ = "ssms_fees_to_be_paid"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    class_id = db.Column(
        db.Integer, db.ForeignKey("ssms_class.id", ondelete="cascade"), nullable=False
    )
    academic_year_id = db.Column(
        db.Integer,
        db.ForeignKey("ssms_academic_year.id", ondelete="cascade"),
        nullable=False,
    )

    @classmethod
    def find_fees_to_be_paid(cls, academic_year_id: int, class_id: int):
        return cls.query.filter_by(academic_year_id=academic_year_id, class_id=class_id)
