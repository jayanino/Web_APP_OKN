class Config(object):
    DEBUG = False
    TESTING = False

    #Add a secret key
    SECRET_KEY = "Secret_KEY"
    FILEPATH="../WEB_APP_OKN/app/static/temp_files"
    #FILEPATH="app/static/temp_files"
    VID_EXTENSION=["MP4","MOV"]
    MAX_FILE_SIZE = 250000000
    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    MAX_FILE_SIZE = 220000000

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    
class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
