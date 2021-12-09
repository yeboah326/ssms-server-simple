# Method to populate the database from json data
# 1 - Check the format of the json data
# {
#     "name_of_class": {
#     "name": "class_name",
#     "fees_to_be_paid": "fees_to_be_paid",
#     "student_list": ["name_of_students"]
# }
# }
import json
from api import db
from api.student.models import Student
from api.fees.models import FeesToBePaid
from api.school.models import AcademicYear, Class
from typing import List


def populate_database(student_data: dict, academic_year_id: int):
    """
    populate_database - Populates the database when provided a json file and the
                        academic year id

    student_data Format
    {
        "name_of_class": {
            "name": "class_name",
            "fees_to_be_paid": Float,
            "student_list": List[str]
            }
    }
    """
    for class_name, class_details in student_data.items():
        # Create temporary instance of the class
        temp_class = Class(
            name=class_details["name"], academic_year_id=academic_year_id
        )
        db.session.add(temp_class)
        db.session.flush()

        # Create the fee instance
        fees_to_be_paid = FeesToBePaid(
            amount=class_details["fees_to_be_paid"],
            class_id=temp_class.id,
            academic_year_id=academic_year_id,
        )

        db.session.add(fees_to_be_paid)
        db.session.flush()

        # Add the list of students to the class
        for student in class_details["student_list"]:
            db.session.add(Student(name=student["name"], class_id=temp_class.id))
            db.session.flush()

    # Store the data permanently
    db.session.commit()

    return "Completed database population successfully"


def move_to_next_term(current_academic_year_id: int, new_academic_year_name: str):
    """
    current_academic_year_id - holds the id of the current academic year
    new_academic_year_name (Year - Term {number}) - name of the new academic year to be created

    classes_to_be_moved -  a list of the ids of the classes to be moved
    """
    # Get the current academic year
    current_academic_year = AcademicYear.find_by_id(current_academic_year_id)
    # Create the new term(academic_year)
    academic_year = AcademicYear(
        name=new_academic_year_name, school_id=current_academic_year.school_id
    )

    # Store the term (academic year) temporarily
    db.session.add(academic_year)
    db.session.flush()

    # Retrieve all the classes in the current academic year
    classes = Class.query.filter_by(academic_year_id=current_academic_year_id).all()

    for school_class in classes:
        migrate_class_to_new_academic_year(academic_year, school_class)

    db.session.commit()


def migrate_class_to_new_academic_year(academic_year: AcademicYear, old_class: Class):
    # Create class in the new academic year
    school_class = Class(name=old_class.name, academic_year_id=academic_year.id)

    db.session.add(school_class)
    db.session.flush()

    # Create fees to be paid for the class
    fees_to_be_paid = FeesToBePaid(
        amount=old_class.fees_to_be_paid,
        class_id=school_class.id,
        academic_year_id=academic_year.id,
    )

    db.session.add(fees_to_be_paid)
    db.session.flush()

    # Migrate the students too
    # Retrieve all students
    students = Student.query.filter_by(class_id=old_class.id).all()

    # Create new instances of students
    for student in students:
        new_student = Student(
            name=student.name,
            date_of_birth=student.date_of_birth,
            class_id=school_class.id,
        )
        db.session.add(new_student)
        db.session.flush()
