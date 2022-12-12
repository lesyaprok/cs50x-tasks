import os
import time

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
    user_purchase = db.execute(
        "SELECT symbol, SUM(shares) as shares, price FROM purchase_track WHERE user_id=? GROUP BY symbol", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
    grand_total = cash

    # if not user_purchase[0]["symbol"] and not user_purchase[0]["shares"] and not user_purchase[0]["price"]:
    #     user_purchase = []
    for i in range(len(user_purchase)):
        user_purchase[i]["company_name"] = lookup(user_purchase[i]["symbol"])["name"]
        user_purchase[i]["total"] = float(user_purchase[i]["shares"]) * user_purchase[i]["price"]
        grand_total += user_purchase[i]["total"]

    return render_template("index.html", user_purchase=user_purchase, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Type positive number")
        user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

        if not symbol or not shares:
            return apology("Type a symbol and number of shares")
        elif shares < 1:
            return apology("Type positive number")

        result = lookup(symbol)
        if not result:
            return apology("Incorrect symbol")

        price = result["price"]
        total = price * float(shares)
        if (user_cash < total):
            return apology("Not enough money")

        timestamp = time.time()
        updated_cash = user_cash - total

        db.execute("UPDATE users SET cash = ? WHERE id=?", updated_cash, session["user_id"])
        db.execute("INSERT INTO purchase_track (user_id, symbol, price, shares, timestamp) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], result["symbol"], price, shares, timestamp)
        return redirect("/")
    # return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_transactions = db.execute("SELECT * FROM purchase_track WHERE user_id=?", session["user_id"])

    for row in user_transactions:
        time_object = time.localtime(row["timestamp"])
        row["timestamp"] = f"{time_object[0]}-{time_object[1]}-{time_object[2]} {time_object[3]}:{time_object[4]:0<2}"

    return render_template("history.html", user_transactions=user_transactions)


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
    if request.method == "GET":
        return render_template("quote.html")
    else:
        user_symbol = request.form.get("symbol").upper()
        result = lookup(user_symbol)
        if not result:
            return apology("Incorrect symbol")
        name, price, symbol = result["name"], result["price"], result["symbol"]
        return render_template("quoted.html", name=name, price=price, symbol=symbol)
    return apology("TODO")


def password_validation(password):
    symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "-", "+"]
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    has_symbol = False
    has_number = False

    if len(password) < 8:
        return False
    for i in password:
        if i in symbols:
            has_symbol = True
        if i in numbers:
            has_number = True
    return has_symbol and has_number


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # check username and password
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password:
            return apology("Check username and password")
        elif not password_validation(password):
            return apology("Your password is not safe, choose another")
        elif not (password == confirmation):
            return apology("Passwords do not match")

        # check if username is already exist
        rows = db.execute("SELECT username FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("Username is already exist")
        # generate password
        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash_password)
        user_id = db.execute("SELECT id FROM users WHERE username=?", username)
        user_id = user_id[0]["id"]
        session["user_id"] = user_id
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        symbols = db.execute(
            "SELECT symbol FROM purchase_track WHERE user_id=? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", symbols=symbols)
    else:
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Type positive number")
        user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

        if not symbol or not shares:
            return apology("Select a symbol and number of shares")
        elif shares < 1:
            return apology("Type positive number")

        user_shares = db.execute(
            "SELECT SUM(shares) as shares FROM purchase_track WHERE user_id=? AND symbol=?", session["user_id"], symbol)[0]["shares"]
        if user_shares < shares:
            return apology("Not enough shares of the stock")

        result = lookup(symbol)
        if not result:
            return apology("Incorrect symbol")

        price = float(result["price"])
        total = price * shares

        timestamp = time.time()
        updated_cash = user_cash + total

        db.execute("UPDATE users SET cash = ? WHERE id=?", updated_cash, session["user_id"])
        db.execute("INSERT INTO purchase_track (user_id, symbol, price, shares, timestamp) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], result["symbol"], price, -(shares), timestamp)
        return redirect("/")
