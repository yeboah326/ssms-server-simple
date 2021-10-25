from api import db

class Expenditure(db.Model):
    __tablename__ = "ssms_expenditure"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255))
    amount = db.Column(db.Float)
    academic_year_id = db.Column(db.Integer, db.ForeignKey("ssms_academic_year.id"), nullable=False)
