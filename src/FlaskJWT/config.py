"""Config settings for for development, testing and production environments."""
import os
from pathlib import Path


HERE = Path(__file__).parent
SQLITE_DEV = "sqlite:///" + str(HERE / "FlaskJWT_db_dev.db")
SQLITE_TEST = "sqlite:///" + str(HERE / "FlaskJWT_test.db")
PROD_DB_USER = os.getenv("DB_USER")
PROD_DB_PASSWORD = os.getenv("DB_PASSWORD")
PROD_DB_NAME = os.getenv("DB_NAME")
PROD_DB_PORT = os.getenv("DB_PORT")
PROD_DB_HOST = os.getenv("DB_HOST")
PROD_DB_URL = f"postgresql+psycopg2://{PROD_DB_USER}:{PROD_DB_PASSWORD}@{PROD_DB_HOST}:{PROD_DB_PORT}/{PROD_DB_NAME}"


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "A-secret-key")
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0
    REFRESH_TOKEN_EXPIRE_HOURS = 0
    REFRESH_TOKEN_EXPIRE_MINUTES = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = SQLITE_TEST


class DevelopmentConfig(Config):
    """Development configuration."""

    TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_MINUTES = 30
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_DEV)


class ProductionConfig(Config):
    """Production configuration."""

    TOKEN_EXPIRE_HOURS = 1
    REFRESH_TOKEN_EXPIRE_HOURS = 720
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", PROD_DB_URL)
    PRESERVE_CONTEXT_ON_EXCEPTION = True


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def getConfig(configName):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(configName, ProductionConfig)
