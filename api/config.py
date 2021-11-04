"""Configuration for development, testing and production"""
import os
from dotenv import load_dotenv
from datetime import timedelta

# Loading virtual environment variables
load_dotenv()

DATABASE_TEST = os.getenv("DATABASE_TEST_URL", "Test_DB_URL")
# Taking of SQLAlchemy 1.4+ compatibility issues on Heroku
if DATABASE_TEST.startswith("postgres://"):
    DATABASE_TEST = DATABASE_TEST.replace("postgres://", "postgresql://", 1)

DATABASE_PROD = os.getenv("DATABASE_URL", "Prod_DB_URL")
# Taking of SQLAlchemy 1.4+ compatibility issues on Heroku
if DATABASE_PROD.startswith("postgres://"):
    DATABASE_PROD = DATABASE_PROD.replace("postgres://", "postgresql://", 1)


class Config:
    """Base Configuration"""

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing Configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = DATABASE_TEST


class ProductionConfig(Config):
    """Production Configuration"""

    SQLALCHEMY_DATABASE_URI = DATABASE_PROD
