from api import db


class Student(db.Model):
    __tablename__ = "ssms_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey("ssms_class.id"), nullable=False)
    fees = db.relationship("Fees", backref="student", lazy=True)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
