from api import db

class Student(db.Model):
    __tablename__ = "ssms_student"
    id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey("ssms_class.id"), nullable=False)
    fees = db.relationship("Fees", backref="student", lazy=True)
