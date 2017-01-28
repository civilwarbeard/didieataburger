import os

from flask import Flask

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "didieataburger.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import controller
from . import login
from . import filters
#remove below if doesn't work

if __name__ == '__main__':
	app.debug = True
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)