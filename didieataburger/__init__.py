import os

from flask import Flask

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "didieataburger.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import controller
from . import filters
from . import login

