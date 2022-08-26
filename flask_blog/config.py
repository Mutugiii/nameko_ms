import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    '''
    General configurations that are inherited by the other classes
    '''
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('FLASK_JWT_SECRET_KEY')
    AMQP_URI = f"amqp://{os.getenv('RABBIT_USER')}:{os.getenv('RABBIT_PASSWORD')}@{os.getenv('RABBIT_HOST')}:{os.getenv('RABBIT_PORT')}/"


class ProdConfig(Config):
    '''
    Configurations for application development phase
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_DATABASE_URL")


class DevConfig(Config):
    '''
    Configurations for when app is in development
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("FLASK_TRACK_MODIFICATIONS")
    DEBUG = os.environ.get("FLASK_DEBUG")

class TestConfig(Config):
    '''
    Configuration class for application testing
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_TEST_DATABASE_URL")
    DEBUG = os.environ.get("FLASK_DEBUG")

config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig
}