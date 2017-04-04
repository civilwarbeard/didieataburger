from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from . import app
from flask_login import UserMixin

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

Base = declarative_base()
Base.metadata.bind = engine
#Session = sessionmaker(bind=engine)
#session = Session()
db_session = scoped_session(sessionmaker(autocommit=False,
							autoflush=False,
							bind=engine))

Base.query = db_session.query_property()
Base.metadata.create_all(engine)

class Eater(Base, UserMixin):
	__tablename__ = "eater"

	id = Column(Integer, primary_key=True)
	first_name = Column(String, default="None")
	last_name = Column(String, default="None")
	username = Column(String, nullable=False)
	password = Column(String(128), nullable=False)
	is_active = Column(Boolean, default=True)

	burgers = relationship("Burger", backref="burger_eater")

class Burger(Base):
	__tablename__ = "burger"

	id = Column(Integer, primary_key=True)
	time_eaten = Column(DateTime, default=datetime.utcnow)

	eater = Column(Integer, ForeignKey("eater.id"), nullable=False)

#Base.metadata.create_all(engine)