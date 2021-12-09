# Testing the database population and migration methods
import os
import json
from api.utils.utils import populate_database, move_to_next_term
from api.tests.utils_test import (
    db_reset,
    create_super_user,
    create_school,
    create_teacher,
    create_academic_year,
    create_class,
)


def test_populate_database(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    teacher = create_teacher(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, super_user, school)

    # Create a class
    school_class = create_class(client, super_user, academic_year, 500)

    # Load json data
    cwd = os.getcwd()
    with open(cwd + "/api/tests/data/sample_database_population_data.json") as f:
        student_data = json.load(f)

    populate_database(student_data=student_data, academic_year_id=academic_year.id)

    # Reset the database
    db_reset()


def test_move_to_next_term(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    teacher = create_teacher(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, super_user, school)

    # Create a class
    school_class = create_class(client, super_user, academic_year, 500)

    # Load json data
    cwd = os.getcwd()
    with open(cwd + "/api/tests/data/sample_database_population_data.json") as f:
        student_data = json.load(f)

    populate_database(student_data=student_data, academic_year_id=academic_year.id)

    move_to_next_term(
        current_academic_year_id=academic_year.id,
        new_academic_year_name="2018 - Term 2",
    )

    # Reset the database
    db_reset()
