import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_URL = '0.0.0.0'
    SERVER_PORT = 8080


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'dev.sqlite')
    GOOGLE_ID = '437300907319-oortl8ku5vcj5vei7g16o6e0trt6mcea.apps.googleusercontent.com'
    GOOGLE_SECRET = 'EMglpZxAsaffaxYa0KP3hPXJ'

class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://item_catalog:udacity@localhost:5432/catalog'
    GOOGLE_ID = '437300907319-d0emuuj479l6a4b90jllvqcie2bfndo2.apps.googleusercontent.com'
    GOOGLE_SECRET = 'iPYhAHzKmcl1Ucy0GThXfFxk'

