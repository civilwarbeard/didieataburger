import os
from flask_script import Manager

from blog import app
from blog.database import session, Entry, User, Base

from getpass import getpass

from werkzeug.security import generate_password_hash

manager = Manager(app)

@manager.command
def run():
	port = int(os.environ.get('PORT', 2424))
	app.run(host='0.0.0.0', port=port)
    
if __name__ == "__main__":
    manager.run()