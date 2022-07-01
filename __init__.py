def getApp():
    return app

import os
import json
import requests
import datetime as dt

from cs50 import SQL
from tempfile import mkdtemp
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Ensure templaets are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 libary to use SQLite database
db = SQL("DATABASE_URL")

# Set time
time_today = dt.datetime.now()
hour_time = dt.datetime.now().hour

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    url = "https://dailyprayer.abdulrcs.repl.co/api/bangkok"
    response = requests.get(url)
    DATA = response.json()
    #Send TODO data that user type in to index.html
    return render_template("prayer.html", data = DATA, hour_time = hour_time, time_today = time_today)


@app.route ("/todo", methods=["GET", "POST"])
@login_required
def todo():
    if request.method == "POST":

        # Add the user's entry into the database
        session_user_id = session["user_id"]
        task = request.form.get("task")
        #Check if user provided input
        if not task:
            return apology("must provide task!", 400)

        #Remember birthdays
        db.execute("INSERT INTO todo (person_id, task) VALUES(?, ?)", session_user_id, task)
        return redirect("/todo")

    else:
        # Display the entries in the database on index.html
        session_user_id = session["user_id"]
        TODO = db.execute("SELECT * FROM todo WHERE person_id = ?", session_user_id)
        #Send TODO data that user type in to index.html
        return render_template("index.html", todo = TODO)




@app.route ("/login", methods=["GET", "POST"])
def login():


    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST (Login form))
    if request.method == "POST":

        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return apology("must provide username and password", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/todo")
    
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """"Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/todo")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        #Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("must provide information", 400)

        #define usernamedatabase to check if username already exist or not
        database = db.execute("SELECT username FROM users WHERE username = ?", username)
        username_database = "a"
        for i in range(len(database)):
            username_database = database[i]["username"]
        if username == username_database:
            return apology("username already exist")

        #Ensure password and confirmation are correct
        elif password != confirmation:
            return apology("password and confirmation aren't match")

        #get information from user to database

        #use hash function to generate password to hash before insert into database
        hash = generate_password_hash(password)
        registrants = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        return render_template("login.html")

    else:
        return render_template("register.html")

@app.route("/delete", methods=["POST"])
def delete():
    #Delete birthdays
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM todo WHERE id = ?", id)
    return redirect("/todo")
