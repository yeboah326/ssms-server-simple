from api import db

class School(db.Model):
    __tablename__ = "ssms_school"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    location = db.Column(db.String(100), nullable=True, unique=False)
    expenditures = db.relationship("Expenditure", backref="school", lazy=True, cascade="all, delete")
    users = db.relationship("SchoolUser", backref="school", lazy=True, cascade="all, delete")

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def retrieve_all_expenditures(cls, id):
        return cls.query.filter_by(id=id).first().expenditures

    @classmethod
    def modify_school_name(cls, new_name):
        pass


    @classmethod
    def modify_school_location(cls, new_location):
        pass