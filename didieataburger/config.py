import os

class DevelopmentConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgres://dycyenkhzpwrpr:4922ccce654d5d79d4e4a264b85ad973f9b4d71c22f619e5668365bad4a9a587@ec2-54-163-224-108.compute-1.amazonaws.com:5432/dac17q38527sv4"
	DEBUG = True
	SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))
