import datetime
from api import db
from dataclasses import dataclass


@dataclass
class Expenditure(db.Model):
    id: int
    description: str
    amount: float
    date_created: datetime.date
    academic_year_id: int

    __tablename__ = "ssms_expenditure"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.Date(), default=datetime.date.today(), nullable=True)
    academic_year_id = db.Column(
        db.Integer,
        db.ForeignKey("ssms_academic_year.id", ondelete="cascade"),
        nullable=False,
    )

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
