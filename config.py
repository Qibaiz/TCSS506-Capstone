
class Config(object):
    # SECRET KEY
    SECRET_KEY = 'A_VERY_LONG_SECRET'

    # DATABASE configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///login.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False