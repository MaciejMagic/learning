import os

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

    """Odds are youll want to execute multiple SELECTs. Depending on how you implement your table(s),
    you might find GROUP BY HAVING SUM and/or WHERE of interest."""

    """Odds are youll want to call lookup for each stock."""

    return apology("TODO")


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
            return apology("must provide a valid stock symbol")

        # Require that a user input a number of shares, implemented as a field whose name is shares
        nrOfShares = int(request.form.get("shares"))

        # Render an apology if the input is not a positive integer
        if nrOfShares < 0:
            return apology("must provide a positive number")

        stockPrice = buyStock["price"]
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        userCash = user[0]["cash"]
        sharesToBuyTotal = nrOfShares * stockPrice

        # Render an apology, without completing a purchase, if the user cannot afford the number of shares at the current price
        if sharesToBuyTotal < userCash:
            return apology("you do not have funds for this purchase")

        # Substract cash spent from user account
        db.execute("UPDATE users SET cash = ? WHERE user_id = ?", userCash - sharesToBuyTotal, session["user_id"])

        # Add one or more new tables to finance.db via which to keep track of the purchase
        updateSharesTable = db.execute("""INSERT INTO shares
                                       (user_id, symbol, share, price, time)
                                       VALUES (?, ?, ?, ?, ?)""", session["user_id"], buySymbol, nrOfShares, stockPrice, ??? )

        if not updateSharesTable:
            # Define UNIQUE indexes on any fields that should be unique
            # Define (non-UNIQUE) indexes on any fields via which you will search (as via SELECT with WHERE)
            db.execute("""
                CREATE TABLE shares (
                    id INTEGER PRIMARY KEY NOT NULL,
                    user_id INTEGER NOT NULL,
                    symbol TEXT NOT NULL,
                    share INTEGER NOT NULL,
                    price REAL NOT NULL,
                    time TIMESTAMP NOT NULL
                    )""")
            db.execute("""INSERT INTO shares
                       (user_id, symbol, share, price, time)
                       VALUES (?, ?, ?, ?, ?)""", session["user_id"], buySymbol, nrOfShares, stockPrice, ??? )

        # Upon completion, redirect the user to the home page
        return redirect("index.html")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    """For each row, make clear whether a stock was bought or sold and include the stocks symbol,
    the (purchase or sale) price, the number of shares bought or sold,
    and the date and time at which the transaction occurred."""

    """You might need to alter the table you created for buy or supplement it with an additional table. Try to minimize redundancies."""

    return apology("TODO")


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
            return apology("must provide stock symbol")

        # Require that the symbol provided is valid
        quoteResponse = lookup(symbol)

        if not quoteResponse:
            return apology("must provide a valid stock symbol")

        return render_template("quoted.html", name=quoteResponse["name"], symbol=quoteResponse["symbol"], price=quoteResponse["price"])

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Require that a user inputs a username, implemented as a text field whose name is username
        username = request.form.get("username")

        # Render an apology if the user username input is blank
        if not username:
            return apology("must provide a username")

        nameInDb = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Render an apology if the user username input already exists
        if nameInDb:
            return apology("that username is already taken")

        # Require that a user input a password, implemented as a text field whose name is password...
        password = request.form.get("password")

        # Render an apology if the user password input is blank
        if not password:
            return apology("must provide a password")

        # ...and then that same password again, implemented as a text field whose name is confirmation
        confirmation = request.form.get("confirmation")

        # Render an apology if the user password confirmation input is blank
        if not confirmation:
            return apology("must provide a matching password in both boxes")

        # Render an apology if the user password and confirmation input do not match
        if password != confirmation:
            return apology("passwords do not match")

        # Hash the users password with generate_password_hash
        passwordHash = generate_password_hash(password)

        # Insert the new user into users, storing a hash of the users password, not the password itself
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, passwordHash)

        userId = db.execute("SELECT id FROM users WHERE username = ?", username)

        # log user in
        session["user_id"] = userId

        return render_template("index.html")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    
    """Require that a user input a stocks symbol, implemented as a select menu whose name is symbol.
    Render an apology if the user fails to select a stock or if (somehow, once submitted)
    the user does not own any shares of that stock."""

    """Require that a user input a number of shares, implemented as a field whose name is shares.
    Render an apology if the input is not a positive integer or if the user does not own that many shares of the stock."""

    """Submit the users input via POST to /sell."""

    """Upon completion, redirect the user to the home page."""


    return apology("TODO")
