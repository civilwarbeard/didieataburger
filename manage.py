import os
from flask_script import Manager

from didieataburger import app
from didieataburger.database import session, Burger, Eater, Base

from getpass import getpass

from werkzeug.security import generate_password_hash

manager = Manager(app)

@manager.command
def run():
	port = int(os.environ.get('PORT', 2424))
	app.run(host='0.0.0.0', port=port)

@manager.command
def seed():
	nick = Eater(first_name="Nick", last_name="Janquart", username="random1", password="test")
	gemma = Eater(first_name="Gemma", last_name="Petrie", username="pammeg",password="test")
	jer = Eater(first_name="Jer", last_name="Janquart", username="numbnuts", password="test")
	matt = Eater(first_name="Matt", last_name="Obrien", username="matto", password="test")
	rc = Eater(first_name="Ryan", last_name="Cowan", username="rycow", password="test")
	peter = Eater(first_name="Peter", last_name="Compernolle", username="pecomp", password="test")
	karl = Eater(first_name="Karl", last_name="Kell", username="karlk", password="test")
	eric = Eater(first_name="Eric", last_name="Sanders", username="chico", password="test")

	session.add_all([nick, gemma, jer, matt, rc, peter, karl, eric])
	session.commit()

    
if __name__ == "__main__":
    manager.run()