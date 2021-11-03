from api import db
from sqlalchemy.sql import func
from api.fees.models import Fees
from api.school.models import Class
from api.student.models import Student


def check_student_paid_fees_in_full(student_id: int) -> bool:
    """Checks whether the student has paid in full after payment

    Args:
        student_id (int): ID of student whose fee payment is to be created or modified

    Returns:
        bool: A boolean which represents whether a student has paid in full or not
    """
    student = Student.find_by_id(id=student_id)
    fees_to_be_paid = Class.find_by_id(student.class_id).fees_to_be_paid
    fees_paid = db.session.query(
        func.sum(Fees.amount).filter(Fees.student_id == student_id)
    ).all()[0][0]
    paid_in_full = True if fees_paid >= fees_to_be_paid else False

    return {
        "fees_to_be_paid": fees_to_be_paid,
        "fees_paid": fees_paid,
        "paid_in_full": paid_in_full,
    }
