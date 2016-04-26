import os
basedir = os.path.abspath(os.path.dirname(__file__))
import sys
#sys.path.append("/Users/jaropis/Dropbox/praca/software/idaneCMS/app") ## to trzeba z jakiegos powodu pod Makiem dodac ???? :(

print(basedir, "dupa")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tosia'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    IDANE_MAIL_SUBJECT_PREFIX = '[idane.pl]'
    IDANE_MAIL_SENDER = 'idane.pl Jarosław Piskorski <jaropis@idane.pl>'
    IDANE_ADMIN = os.environ.get('IDANE_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'stmp.idane.pl'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig
          }
