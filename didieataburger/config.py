import os

class DevelopmentConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:Cthulhu81@localhost:5432/didieataburger"
	DEBUG = True
	SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))

class HerokuConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgres://jcggpclvndfhjt:bec6ff7d31937d7408f5445dc7b7999d151ce480c5068aabd72828174de1724c@ec2-23-23-225-116.compute-1.amazonaws.com:5432/db7obq9s5jergs"
	DEBUG = True