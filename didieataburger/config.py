import os

class DevelopmentConfig(object):
	app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ubuntu:Cthulhu81@localhost:5432/didieataburger"
	DEBUG = True
	SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))
