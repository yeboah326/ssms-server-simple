from api import db
from dataclasses import dataclass
import datetime


@dataclass
class Student(db.Model):
    id: int
    name: str
    date_of_birth: datetime.date
    class_id: int
    fees_paid_in_full: bool

    __tablename__ = "ssms_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=True)
    class_id = db.Column(
        db.Integer, db.ForeignKey("ssms_class.id", ondelete="cascade"), nullable=False
    )
    fees = db.relationship(
        "Fees",
        backref="student",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True,
    )
    fees_paid_in_full = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
