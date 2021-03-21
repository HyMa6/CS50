import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Put information from 'portfolio' into a list
    # got help from https://cs50.stackexchange.com/questions/30264/pset7-finance-index
    stocks = db.execute("SELECT symbol, shares FROM stocks WHERE user_id = :user",
                          user=session["user_id"])

    # List to add all totals
    total_sum = []

    # Iterate over the stocks list to append the faulty information needed in index.html table
    for stock in stocks:
        symbol = str(stock["symbol"])
        shares = int(stock["shares"])
        name = lookup(symbol)["name"]
        price = lookup(symbol)["price"]
        total = shares * price
        stock["name"] = name
        stock["price"] = usd(price)
        stock["total"] = usd(total)
        total_sum.append(float(total))

    # Store the username of the user logged
    username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"]

    # Declare the cash available and grand total
    cash_available = db.execute("SELECT cash FROM users WHERE username = :username", username=username)[0]["cash"]
    cash_total = sum(total_sum) + cash_available

    return render_template("index.html", stocks=stocks, cash_available=usd(cash_available), cash_total=usd(cash_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Check that symbol is valid
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        # Ensure a valid amount of shares
        if not shares.isdigit():
            return apology("you need to int provide a positive value", 400)
        shares = int(shares)
        if shares <= 0:
            return apology("you need to int provide a positive value", 400)



        # Calculate total value of the transaction
        price=lookup(symbol)['price']
        cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=session["user_id"])[0]['cash']
        cash_after = cash - price * shares

        # Check if current cash is enough for transaction
        if cash_after < 0:
            return apology("You don't have enough money for this transaction")


        # Check if user already has one or more stocks from the same company
        stock = db.execute("SELECT shares FROM stocks WHERE user_id = :user AND symbol = :symbol",
                          user=session["user_id"], symbol=symbol)

        # Insert new row into the stock table
        if not stock:
            db.execute("INSERT INTO stocks(user_id, symbol, shares) VALUES (:user, :symbol, :shares)",
                user=session["user_id"], symbol=symbol, shares=shares)

        # update row into the stock table
        else:
            shares += stock[0]['shares']

            db.execute("UPDATE stocks SET shares = :shares WHERE user_id = :user AND symbol = :symbol",
                user=session["user_id"], symbol=symbol, shares=shares)

        # update user's cash
        db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                          cash=cash_after, user=session["user_id"])

        # Update history table
        db.execute("INSERT INTO history(user_id, symbol, shares, price) VALUES (:user, :symbol, :shares, :price)",
                user=session["user_id"], symbol=symbol, shares=shares, price=round(price*float(shares)))

        # Redirect user to index page with a success message
        flash("Purchase successful!")
        return redirect("/")


    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    operations = db.execute("SELECT * FROM history WHERE user_id=:user_id;", user_id=session["user_id"])

    return render_template("history.html", operations=operations)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        # Ensure that the symbol is provided
        if not symbol:
            return apology("must provide a symbol", 400)
        # Get the quote
        quote = lookup(symbol)
        # Check if is a valid quote
        if not quote:
            return apology("error getting quote", 400)

        return render_template("quoted.html", quote=quote)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html", stock="")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
# User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

                # Ensure confirm password is correct
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("The passwords don't match", 403)

        # Query database for username if already exists
        elif db.execute("SELECT * FROM users WHERE username = :username",
            username=request.form.get("username")):
            return apology("Username already taken", 403)

        # Insert user and hash of the password into the table
        db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)",
            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
            username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")


        # Store the symbol inputed
        look = lookup(request.form.get("symbol"))

        # Store shares inputed
        shares = request.form.get("shares")

        # Store the number of shares the user has
        user_shares = db.execute("SELECT shares FROM stocks WHERE user_id = :username and symbol = :symbol",
                        username=session["user_id"], symbol=str(request.form.get("symbol")))[0]["shares"]


        # Store the value of sale
        value = look["price"] * int(shares)

        # If the symbol searched or number of shares is invalid, return apology
        if not request.form.get("symbol"):
            return apology("you must provide a stock", 400)

        elif not shares or not shares.isdigit() or int(shares) < 1 or int(shares) > int(user_shares):
            return apology("share number is invalid", 400)

        # If everything checks, proceed with sell
        else:
            # Add the value of sale to the user's cash
            db.execute("UPDATE users SET cash = cash + :value WHERE id = :username", value=value, username=int(session["user_id"]))

            # If the user is selling all the shares, remove the stock from the user's stocks
            if int(user_shares) == int(shares):
                db.execute("DELETE FROM stocks WHERE user_id = :username and symbol = :symbol",
                            username=session["user_id"], symbol=str(request.form.get("symbol")))

            # If the user is just selling some of the shares, update the stock
            elif int(user_shares) > int(shares):
                updated_shares= int(user_shares) - int(shares)
                db.execute("UPDATE stocks SET shares = :updated_shares WHERE user_id = :username and symbol = :symbol",
                            updated_shares=int (updated_shares), username=session["user_id"], symbol=request.form.get("symbol"))

            # Update history table
            db.execute("INSERT INTO history(user_id, symbol, shares, price) VALUES (:user, :symbol, :shares, :price)",
                user=session["user_id"], symbol=symbol, shares=shares, price=look["price"])

        # return to root
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Get the symbols from portfolio for the select list
        symbols = db.execute("SELECT symbol FROM stocks WHERE user_id = :username", username=session["user_id"])

        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
