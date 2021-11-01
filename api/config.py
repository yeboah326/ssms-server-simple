"""Configuration for development, testing and production"""
import os
from dotenv import load_dotenv

# Loading virtual environment variables
load_dotenv()

DATABASE_TEST = os.getenv("DATABASE_TEST_URL")
DATABASE_PROD = os.getenv("DATABASE_URL")


class Config:
    """Base Configuration"""

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing Configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = DATABASE_TEST


class ProductionConfig(Config):
    """Production Configuration"""

    SQLALCHEMY_DATABASE_URI = DATABASE_PROD
