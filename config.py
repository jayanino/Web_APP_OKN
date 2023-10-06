class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = "f6f56559b9fed69a471ed9ac9079346e"
    FILEPATH="../WEB_APP_OKN/app/static/temp_files"
    VID_EXTENSION=["MP4","MOV"]
    MAX_FILE_SIZE = 250000000
    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    MAX_FILE_SIZE = 260000000

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    
class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
