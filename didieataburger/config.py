import os

class DevelopmentConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgres://jcggpclvndfhjt:bec6ff7d31937d7408f5445dc7b7999d151ce480c5068aabd72828174de1724c:5432/ec2-23-23-225-116.compute-1.amazonaws.com"
	DEBUG = True
	SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))
