from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, UserMixin, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import app
from .database import session, Eater, Burger



@app.route("/")
def not_logged_in():
	return render_template("landing.html")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/create")
def create():
	return render_template("create.html")