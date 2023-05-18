from email.policy import default
import functools
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template,render_template_string
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from banker.helper import util
from banker.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")
white_list = ["http://google.com"]

"""Redirects users to the login page."""
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

"""Load userid of an user if it is stored in database"""
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )

"""Register user"""
@bp.route("/register", methods=("GET", "POST"))
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        confirm_password = request.form.get("cpassword")
        balance_str = request.form.get("ibalance")
        db = get_db()
        error = None
        if not util.validate_string(username):
            error = "Invalid name. Name are restricted to _, - , . , digits, and lowercase alphabetical characters with 127 max length"
            flash(error)
        if not util.validate_string(password):
            error = "Invalid password. Password are restricted to _ , - , . , digits, and lowercase alphabetical characters with 127 max length"
            flash(error)
        if password != confirm_password:
            error = "Password did not match. Try again."
            flash(error)
        if not firstname:
            flash("Enter first name")
        if not lastname:
            flash("Enter last name")
        if not username:
            error = "Username is required."
            flash(error)
        if not balance_str:
            balance_str = 0
        elif not password:
            error = "Password is required."
            flash(error)
        if not util.validate_balance(balance_str) :
            error = "Invalid balance number, you can enter 0 to 4294967295.99."
            flash(error)
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
        if user:
            print("a register id: ",user["id"])
            error = f"User {username} is already registered."
            flash(error)
        else:
            if not error:
                try:
                    db.execute(
                        "INSERT INTO user (username, password, firstname, lastname, balance) VALUES (?, ?, ?, ?, ?)",
                        (username, generate_password_hash(password), firstname, lastname, float(balance_str)),
                    )
                    db.commit()
                except Exception as e:
                    print(e)
                else:
                    flash("Registration Successful")
                    return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

"""Log in a registered user by adding the user id to the session."""
@bp.route("/login", methods=("GET", "POST"))
def login():
    """
        Vulnerability:
        User can be redirected to any given URL   
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        target = request.args.get('target')
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,), 
        ).fetchone()
        if user is None:
            error = "Wrong username."
        elif not check_password_hash(user["password"], password):
            error = "Wrong password."
        if user:
            session.clear()
            session["user_id"] = user["id"]
            if target and target in white_list:
                return redirect(target)
            else:
                return redirect(url_for('bank.index'))
        flash(error)
    else:
        if session.get("user_id"):
            return redirect(url_for('bank.index'))
    return render_template("auth/login.html")


"""Clear the current session"""
@bp.route("/logout")
def logout():
    if g.user:
        usrname = g.user['username']
    else:
        usrname = "GUEST"
    payload = request.args.get('name',usrname)
    'Vulnerability number 2 server side template injection'
    session.clear()
    return render_template('auth/logout.html', payload=payload)


