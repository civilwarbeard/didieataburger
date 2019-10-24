import os

class DevelopmentConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:PW/didieataburger"
	DEBUG = True
	SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))

class HerokuConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgres://sxarmwdrwkkxns:1b29ad634dac46c7a5246367d32b69884bdb1f31be75c24d2d46d20ede846539@ec2-107-22-236-252.compute-1.amazonaws.com:5432/dbiqc6vqfknu9f"
	DEBUG = True
	SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))
