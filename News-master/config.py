import os

class Config:
    '''
    General configuration parent class
    '''
    ARTICLE_BASE_URL = 'https://newsapi.org/v2/top-headlines?q={}&apiKey={}'
    SEARCH_BASE_URL = 'https://newsapi.org/v2/everything?q={}&apiKey={}'
    SOURCE_ARTICLE_BASE_URL = 'https://newsapi.org/v2/everything?sources={}&apiKey={}'
    SOURCE_BASE_URL ='https://newsapi.org/v2/sources?apiKey={}'
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')

class ProdConfig(Config):
    '''
    Production configuration class

    Args:
        Config: Parent config class with general configurations
    '''
    pass

class DevConfig(Config):
    '''
    Development Configuration class

    Args:
        Config: Parent config class with general configurations
    '''
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}
