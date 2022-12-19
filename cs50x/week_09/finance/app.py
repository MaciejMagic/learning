import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # initialize list of user current stocks (dicts)
    currentStocks = []

    # extract total of user shares for each stock from db (list of dicts)
    portfolio = db.execute("SELECT symbol, SUM(share) FROM shares WHERE user_id = ? GROUP BY symbol", session["user_id"])

    # populate the currentStocks list with user stocks (with latest prices)
    for stock in range(len(portfolio)):

        # for each company (stock) lookup() creates a dict with keys: "name", "price", "symbol"
        currentStocks.append(lookup(portfolio[stock]["symbol"]))

        # adding "shares" key to those dicts
        currentStocks[stock]["shares"] = portfolio[stock]["share"]

        # fetch current user cash
        cash = db.execute("SELECT cash FROM users WHERE user_id = ?", session["user_id"])

    return render_template("index.html", currentStocks, cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Require that a user input a stocks symbol, implemented as a text field whose name is symbol
        buySymbol = request.form.get("symbol")
        buyStock = lookup(buySymbol)

        # Render an apology if the input is blank or the symbol does not exist
        if not buySymbol or not buyStock:
            return apology("must provide a valid stock symbol", 403)

        # Require that a user input a number of shares, implemented as a field whose name is shares
        nrOfShares = int(request.form.get("shares"))

        # Render an apology if the input is not a positive integer
        if nrOfShares < 0:
            return apology("must provide a positive number", 403)

        stockPrice = buyStock["price"]
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        userCash = user[0]["cash"]
        sharesToBuyTotal = nrOfShares * stockPrice

        # Render an apology, without completing a purchase, if the user cannot afford the number of shares at the current price
        if sharesToBuyTotal < userCash:
            return apology("you do not have funds for this purchase", 403)

        # Substract cash spent from user account
        db.execute("UPDATE users SET cash = ? WHERE user_id = ?", userCash - sharesToBuyTotal, session["user_id"])

        # Add one or more new tables to finance.db via which to keep track of the purchase
        updateSharesTable = db.execute("""INSERT INTO shares
                                       (user_id, symbol, share, price, time)
                                       VALUES (?, ?, ?, ?, ?)""", session["user_id"], buySymbol, nrOfShares, stockPrice, datetime.datetime.now())

        if not updateSharesTable:
            # Define UNIQUE indexes on any fields that should be unique / TO DO
            # Define (non-UNIQUE) indexes on any fields via which you will search (as via SELECT with WHERE) / TO DO
            db.execute("""
                CREATE TABLE shares (
                    id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    symbol TEXT NOT NULL,
                    share INTEGER NOT NULL,
                    price REAL NOT NULL,
                    time TIMESTAMP NOT NULL,
                    PRIMARY KEY(id),
                    FOREIGN KEY(user_id) REFERENCES users(id)
                    )""")
            db.execute("""INSERT INTO shares
                       (user_id, symbol, share, price, time)
                       VALUES (?, ?, ?, ?, ?)""", session["user_id"], buySymbol, nrOfShares, stockPrice, datetime.datetime.now())

        # Upon completion, redirect the user to the home page
        return redirect("index.html")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Query db for list of user transactions
    history = db.execute("SELECT symbol, share, price, time FROM shares WHERE user_id = ? ORDER BY time DESC", session["user_id"])

    return render_template("history.html", history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # Require that a user inputs a stocks symbol
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide stock symbol", 403)

        # Require that the symbol provided is valid
        quoteResponse = lookup(symbol)

        if not quoteResponse:
            return apology("must provide a valid stock symbol", 403)

        return render_template("quoted.html", name=quoteResponse['name'], symbol=quoteResponse['symbol'], price=quoteResponse['price'])

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Require that a user inputs a username
        username = request.form.get("username")

        # Render an apology if the user username input is blank
        if not username:
            return apology("must provide a username", 403)

        nameInDb = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Render an apology if the user username input already exists
        if nameInDb:
            return apology("that username is already taken", 403)

        # Require that a user input a password
        password = request.form.get("password")

        # Render an apology if the user password input is blank
        if not password:
            return apology("must provide a password", 403)

        # ...and then that same password again
        confirmation = request.form.get("confirmation")

        # Render an apology if the user password confirmation input is blank
        if not confirmation:
            return apology("must provide a matching password in both boxes", 403)

        # Render an apology if the user password and confirmation input do not match
        if password != confirmation:
            return apology("passwords do not match", 403)

        # Hash the users password with generate_password_hash
        passwordHash = generate_password_hash(password)

        # Add the new user into users, storing a hash of the users password, not the password itself
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, passwordHash)

        userId = db.execute("SELECT id FROM users WHERE username = ?", username)

        # log user in
        session["user_id"] = userId[0]["id"]

        return render_template("index.html")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # Require that a user input a stocks symbol
        sellSymbol = request.form.get("symbol")
        sellStock = lookup(sellSymbol)

        # Render an apology if user didnt select any stock from the list
        if not sellSymbol or sellSymbol == "Symbol":
            return apology("must choose a stock owned from the dropdown list", 403)

        # retrieve user info of shares of the stock provided
        userShares = db.execute("SELECT SUM(share) FROM shares WHERE id = ? AND symbol = ? GROUP BY share", session["user_id"], sellSymbol)

        userSharesNr = int(userShares[0]["share"])

        # Render an apology if user does not have any shares of the provided stock
        if userSharesNr < 1:
            return apology("you do not own any shares of that stock", 403)

        sellUserShares = int(request.form.get("shares"))

        # Render an apology if the input is not a positive integer
        if sellUserShares < 1:
            return apology("must provide a positive number", 403)

        # Render an apology if user does not own that many shares
        if sellUserShares > userSharesNr:
            return apology("must provide a number less than or equal to the shares that you own", 403)

        # Fetch latest stock price
        currentStockPrice = sellStock["price"]

        # Fetch current user account cash balance
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        userCash = user[0]["cash"]

        # Calculate amount of cash for sold shares
        profit = currentStockPrice * sellUserShares

        soldUserShares = sellUserShares - 2 * sellUserShares

        # Substract shares from user portfolio (add entry with negative shares amount to shares table)
        db.execute("""INSERT INTO shares
                      (user_id, symbol, share, price, time)
                      VALUES (?, ?, ?, ?, ?)""", session["user_id"], sellSymbol, soldUserShares, currentStockPrice, datetime.datetime.now())

        # Add cash from sale to user account
        db.execute("UPDATE users SET cash = ? WHERE user_id = ?", userCash + profit, session["user_id"])

        return redirect("index.html")

    # Retrieve a [list] of user shares of [dicts] stocks
    userStocks = db.execute("SELECT symbol, SUM(share) FROM shares WHERE user_id = ? GROUP BY symbol", session["user_id"])

    return render_template("sell.html", userStocks)
