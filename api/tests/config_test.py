import os

def test_app_config(app):
    assert app.config["TESTING"] == True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_TEST_URL")
