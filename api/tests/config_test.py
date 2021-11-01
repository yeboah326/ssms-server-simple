from dotenv import load_dotenv
from api import create_app
import os

load_dotenv()


def test_app_config(app):
    assert app.config["TESTING"] == True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_TEST_URL")


def test_app_testing_config():
    app = create_app("test")
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_TEST_URL")


def test_app_developoment_config():
    app = create_app("prod")
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_URL")
