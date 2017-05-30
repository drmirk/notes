class Config(object):
    '''main config class for configuration'''
    SECRET_KEY = "\xf6Hs\xbe\xd5C'\xde\x88\x8e$\xbc\xfb\xc69m\xd1!\x06\x15\xa0\xc9:\x85\x17\x99\xf1\xfc0\x96\xc8\xbfp\r\x1b`>\x08\xd3\xd6"
    SQLALCHEMY_DATABASE_URI = "sqlite:///mydb.db"

class ProductionConfig(Config):
    '''config class to use in production environment'''
    DEBUG = False

class DevelopmentConfig(Config):
    '''config class to use in development environment'''
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
