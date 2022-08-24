import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    '''
    General configurations that are inherited by the other classes
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

class ProdConfig(Config):
    '''
    Configurations for application development phase
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):
    '''
    Configurations for when app is in development
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("TRACK_MODIFICATIONS")
    DEBUG = os.environ.get("DEBUG")

class TestConfig(Config):
    '''
    Configuration class for application testing
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")
    DEBUG = os.environ.get("DEBUG")

config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig
}