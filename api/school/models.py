from api import db
from dataclasses import dataclass
from api.fees.models import FeesToBePaid
from api.student.models import Student


@dataclass
class School(db.Model):
    id: int
    name: str
    location: str

    __tablename__ = "ssms_school"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    location = db.Column(db.String(100), nullable=True, unique=False)
    academic_years = db.relationship(
        "AcademicYear", backref="school", cascade="all, delete", passive_deletes=True
    )
    users = db.relationship(
        "SchoolUser",
        backref="school",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True,
    )

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def retrieve_all_expenditures(cls, id):
        return cls.query.filter_by(id=id).first().expenditures


@dataclass
class AcademicYear(db.Model):
    id: int
    name: str
    school_id: int

    __tablename__ = "ssms_academic_year"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    school_id = db.Column(
        db.Integer, db.ForeignKey("ssms_school.id", ondelete="cascade"), nullable=False
    )
    classes = db.relationship(
        "Class",
        backref="academic_year",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True,
    )
    fees_to_be_paid = db.relationship(
        "FeesToBePaid",
        backref="academic_year",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True,
    )
    expenditure_types = db.relationship(
        "ExpenditureType",
        backref="academic_year",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True,
    )

    @classmethod
    def find_by_id(cls, academic_year_id):
        return cls.query.filter_by(id=academic_year_id).first()


@dataclass
class Class(db.Model):
    id: int
    name: str
    academic_year_id: int
    fees_to_be_paid: float
    num_students_in_class: int
    num_students_with_arrears: int
    num_students_fully_paid: int

    __tablename__ = "ssms_class"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    academic_year_id = db.Column(
        db.Integer,
        db.ForeignKey("ssms_academic_year.id", ondelete="cascade"),
        nullable=False,
    )
    students = db.relationship(
        "Student",
        backref="class",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True,
    )
    fees_to_be_paid = db.relationship(
        "FeesToBePaid",
        backref="class",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Year: {AcademicYear.find_by_id(self.academic_year_id)}, Class: {self.name}>"

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @property
    def fees_to_be_paid(self):
        return (
            FeesToBePaid.find_fees_to_be_paid(self.academic_year_id, self.id)
            .first()
            .amount
        )

    @property
    def num_students_in_class(self):
        return Student.query.filter_by(class_id=self.id).count()

    @property
    def num_students_with_arrears(self):
        return Student.query.filter_by(
            class_id=self.id, fees_paid_in_full=False
        ).count()

    @property
    def num_students_fully_paid(self):
        return Student.query.filter_by(class_id=self.id, fees_paid_in_full=True).count()
