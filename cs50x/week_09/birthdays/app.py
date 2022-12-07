import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database

        # data from form submission
        fname = request.form.get("name")
        fmonth = request.form.get("month")
        fday = request.form.get("day")
        
        # insert user form data to the database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", fname, fmonth, fday)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html

        # query the database for all entries
        blist = db.execute("SELECT * FROM birthdays")

        # return with the data passed into startpage
        return render_template("index.html", blist=blist)


