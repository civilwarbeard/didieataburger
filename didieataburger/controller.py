from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, UserMixin, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import app
from .database import session, Eater, Burger


@app.route("/")
def not_logged_in():
	return render_template("landing.html")


@app.route("/login", methods=["GET"])
def login_get():
	return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
	"""Login and redirect to to either eat or ate templates"""
	username = request.form["username"]
	password = request.form["password"]
	eater = session.query(Eater).filter_by(username=username).first()

	if not eater or not check_password_hash(eater.password, password):
		return redirect(url_for("login_get"))

	login_user(eater)

	#get login user eat count
	burger_eater = current_user.id
	burger_count = session.query(Burger).filter(burger_eater==Burger.eater).count()

	#get time right now and time last eaten
	burger_day = datetime.today()
	six_days = timedelta(days=6)

	good_to_eat = burger_day - six_days

	#convert datetime for comparison
	burger_day = burger_day.strftime("%Y/%m/%d")
	good_to_eat = good_to_eat.strftime("%Y/%m/%d")

	#grab the last time burger was eaten by logged in user
	last_date_eaten = session.query(Burger).filter(burger_eater==Burger.eater).order_by(\
		Burger.time_eaten.desc()).limit(1)

	#convert burger time from tuple
	last_date_eaten = last_date_eaten[0].time_eaten.strftime("%Y/%m/%d")

	burgers_this_week_count = session.query(Burger).filter(burger_eater==Burger.eater).\
		filter(Burger.time_eaten > good_to_eat).count()

	#check if user ate a burger this week and redirect accordingly
	#****add burgers this week from ate route
	if burgers_this_week_count >= 1:
		return redirect(url_for("ate"))

	return redirect(url_for("eat"))


@app.route("/create", methods=["GET"])
def create():
	return render_template("create.html")


@app.route("/create", methods=["POST"])
def create_post():
	eater = Eater(
		first_name = request.form["first_name"],
		last_name = request.form["last_name"],
		username = request.form["username"],
		password = generate_password_hash(request.form["password"]),
		)

	session.add(eater)
	session.commit()
	login_user(eater)
	return redirect(url_for("eat"))


@app.route("/eat", methods=["GET"])
@login_required
def eat():
	return render_template("eatburger.html")


@app.route("/eat", methods=["POST"])
@login_required
def eat_post():
	#enter burger query update
	burger_eater = current_user.id

	session.add(Burger(eater=burger_eater))

	session.commit()
	return redirect(url_for("ate"))


@app.route("/ate", methods=["GET"])
@login_required
def ate():
	"""The functions here return values and everything else for ate_burger, 
	ate_many templates"""

	burger_eater = current_user.id
	burger_count = session.query(Burger).filter(burger_eater==Burger.eater).count()

	#get time right now and time last eaten
	burger_day = datetime.today()
	six_days = timedelta(days=6)

	good_to_eat = burger_day - six_days

	burgers = session.query(Burger).filter(burger_eater==Burger.eater)
	burgers = burgers.order_by(Burger.time_eaten.desc())

	historical_burgers = session.query(Burger).filter(burger_eater==Burger.eater).\
		filter(Burger.time_eaten < good_to_eat)
	historical_burgers_count = session.query(Burger).filter(burger_eater==Burger.eater).\
		filter(Burger.time_eaten < good_to_eat).count()

	burgers_this_week = session.query(Burger).filter(burger_eater==Burger.eater).\
		filter(Burger.time_eaten > good_to_eat)
	burgers_this_week_count = session.query(Burger).filter(burger_eater==Burger.eater).\
		filter(Burger.time_eaten > good_to_eat).count()

	burger_one = burgers.order_by(Burger.time_eaten.desc()).first()

	#convert datetime for comparison
	burger_day = burger_day.strftime("%Y/%m/%d")
	good_to_eat = good_to_eat.strftime("%Y/%M/%d")

	#grab the last time burger was eaten by logged in user
	last_date_eaten = session.query(Burger).filter(burger_eater==Burger.eater).order_by(\
		Burger.time_eaten.desc()).limit(1)

	#convert burger time from tuple
	last_date_eaten = last_date_eaten[0].time_eaten.strftime("%Y/%M/%d")

	if burgers_this_week_count == 1:
		return render_template("ate_burger.html",
			burgers=burgers,
			burger_one=burger_one,
			burger_eater=burger_eater,
			historical_burgers=historical_burgers,
			historical_burgers_count=historical_burgers_count)

	if burgers_this_week_count > 1:
		return render_template("ate_many.html",
			burgers=burgers,
			burger_count=burger_count,
			burger_eater=burger_eater,
			historical_burgers=historical_burgers,
			burgers_this_week=burgers_this_week,
			burgers_this_week_count=burgers_this_week_count,
			historical_burgers_count=historical_burgers_count)

	return render_template("eatburger.html",
		burgers=burgers,
		burger_eater=burger_eater,
		burgers_this_week=burgers_this_week,
		historical_burgers=historical_burgers,
		historical_burgers_count=historical_burgers_count)


@app.route("/ate", methods=["POST"])
@login_required
def ate_post():
	burger_eater = current_user.id

	session.add(Burger(eater=burger_eater))

	session.commit()
	return redirect(url_for("ate"))


@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("not_logged_in"))
	

@app.route("/settings", methods=["GET"])
@login_required
def settings():
	eater=session.query(Eater).filter(current_user.id==Eater.id)
	eater=eater.one()

	return render_template("settings.html",
		eater=eater)


@app.route("/settings", methods=["POST"])
@login_required
def settings_update():
	eater=session.query(Eater).filter(current_user.id==Eater.id)

	eater=session.query(Eater).filter(current_user.id==Eater.id).update(\
		{"first_name": request.form["first_name"],\
		"last_name": request.form["last_name"],\
		"username": request.form["username"],
		"password": request.form["password"]})

	session.commit()

	return redirect(url_for("ate"))

@app.route("/allburgers", methods=["GET"])
@login_required
def allburgers():
	"""Burger Log for User"""
	burger_eater = current_user.id
	burgers = session.query(Burger).filter(burger_eater==Burger.eater)
	burgers = burgers.order_by(Burger.time_eaten.desc())
	burger_count = session.query(Burger).filter(burger_eater==Burger.eater).count()

	return render_template("allburgers.html",
		burgers=burgers,
		burger_count=burger_count)
