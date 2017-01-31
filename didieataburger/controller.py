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
	username = request.form["username"]
	password = request.form["password"]
	eater = session.query(Eater).filter_by(username=username).first()
	if not eater or not check_password_hash(eater.password, password):
		return redirect(url_for("login_get"))

	login_user(eater)
	return redirect(request.args.get('next') or url_for("eat"))

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
	return redirect(request.args.get('next') or url_for("eat"))

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
	burger_eater = current_user.id
	burger_count = session.query(Burger).filter(burger_eater==Burger.eater).count()

	burgers = session.query(Burger).filter(burger_eater==Burger.eater)
	burgers = burgers.order_by(Burger.time_eaten.desc())
	if burger_count > 1:
		return render_template("ate_many.html",
			burgers=burgers,
			burger_count=burger_count,
			burger_eater=burger_eater)
	return render_template("ate_burger.html",
		burgers=burgers,
		burger_eater=burger_eater)

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



