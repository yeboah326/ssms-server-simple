from api import db

class Fees(db.Model):
    __tablename__ = "ssms_fees"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("ssms_student.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("ssms_class.id"), nullable=False)
