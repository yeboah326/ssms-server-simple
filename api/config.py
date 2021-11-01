"""Configuration for development, testing and production"""
import os

DATABASE_TEST = os.getenv("DATABASE_TEST_URL")
DATABASE_DEV = os.getenv("DATABASE_URL")
DATABASE_PROD = os.getenv("DATABASE_PROD_URL")


class Config:
    """Base Configuration"""

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing Configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = DATABASE_TEST


class DevelopmentConfig(Config):
    """Development Configuration"""

    SQLALCHEMY_DATABASE_URI = DATABASE_DEV


class ProductionConfig(Config):
    """Production Configuration"""

    SQLALCHEMY_DATABASE_URI = DATABASE_PROD


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)
