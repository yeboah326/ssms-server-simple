import datetime
from api import db
from dataclasses import dataclass


@dataclass
class Expenditure(db.Model):
    id: int
    description: str
    amount: float
    date: str
    expenditure_type_id: int

    __tablename__ = "ssms_expenditure"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.Date(), default=datetime.date.today(), nullable=True)
    expenditure_type_id = db.Column(
        db.Integer,
        db.ForeignKey("ssms_expenditure_type.id", ondelete="cascade"),
        nullable=False,
    )

    @property
    def date(self):
        return self.date_created.strftime("%d-%m-%Y")

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


@dataclass
class ExpenditureType(db.Model):
    id: int
    name: int
    academic_year_id: int

    __tablename__ = "ssms_expenditure_type"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    expenditures = db.relationship(
        "Expenditure",
        backref="expenditure_type",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True,
    )
    academic_year_id = db.Column(
        db.Integer,
        db.ForeignKey("ssms_academic_year.id", ondelete="cascade"),
        nullable=False,
    )

    @classmethod
    def find_by_academic_year_id(cls, academic_year_id):
        return cls.query.filter_by(academic_year_id=academic_year_id).all()
