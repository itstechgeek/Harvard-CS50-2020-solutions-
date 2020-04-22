import os
from datetime import datetime
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
app.jinja_env.globals.update(usd=usd)

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
    # current user's stock holdings
    user_id = session["user_id"]
    rows = db.execute("SELECT symbol, number_of_shares FROM user_stock_info WHERE user_id=:user_id", user_id=user_id)
    sum_stocks = 0
    # add current price and total value to the rows table
    for row in rows:
        stock_info = lookup(row["symbol"])
        current_price = stock_info["price"]
        row["symbol"] = row["symbol"].upper()
        row["current_price"] = current_price
        row["total_value"] = round(current_price * row["number_of_shares"], 2)
        sum_stocks += row["total_value"]

    sum_stocks = round(sum_stocks, 2)
    user_cash = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=user_id)[0]["cash"]
    net_value = round(user_cash + sum_stocks, 2)

    return render_template("index.html", user_stocks=rows, sum_stocks=sum_stocks, net_value=net_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        symbol = request.form.get("symbol")
        number_of_shares_string = request.form.get("shares")
        if symbol == "":
            return apology("symbol empty")
        if number_of_shares_string == "":
            return apology("number of shares empty")

        # check for non numeral shares
        try:
            number_of_shares = int(number_of_shares_string)
        except:
            return apology("enter a positive number for shares")

        number_of_shares = int(number_of_shares_string)
        if number_of_shares < 1:
            return apology("enter a positive number for shares")

        stock_info = lookup(symbol)
        if not stock_info:
            return apology("stock code invalid")

        # check if user can buy the stock
        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=user_id)[0]["cash"]

        # total value of stock being bought
        total_value = stock_info["price"] * number_of_shares

        # cash balance left with the user
        balance = user_cash - total_value

        if balance >= 0:
            # insert the bought record into stock_history
            db.execute("INSERT INTO stock_trade_history (user_id, symbol, price, buy_or_sell, number_of_shares, datetime) VALUES (:user_id, :symbol, :price, :buy_or_sell, :number_of_shares, :datetime)", user_id=user_id, symbol=symbol, price=stock_info["price"], buy_or_sell="bought", number_of_shares=number_of_shares, datetime=datetime.now())

            rows = db.execute("SELECT * FROM user_stock_info WHERE user_id=:user_id and symbol=:symbol", user_id=user_id, symbol=symbol)
            # if user already has the stock being bought (i.e. rows > 0)
            if len(rows) > 0:
                # update the user_stock_info table
                total_shares = number_of_shares + db.execute("SELECT number_of_shares FROM user_stock_info WHERE user_id=:user_id and symbol=:symbol", user_id=user_id, symbol=symbol)[0]["number_of_shares"]
                total_value = total_shares * stock_info["price"]
                db.execute("UPDATE user_stock_info SET number_of_shares=:total_shares, total_value=:total_value WHERE user_id=:user_id and symbol=:symbol", total_shares=total_shares, total_value=total_value, user_id=user_id, symbol=symbol)

            else:
                # else insert into user_stock_info table
                db.execute("INSERT INTO user_stock_info (user_id, symbol, number_of_shares, current_price, total_value) VALUES (:user_id, :symbol, :number_of_shares, :current_price, :total_value)", user_id=user_id, symbol=symbol, number_of_shares=number_of_shares, current_price=stock_info["price"], total_value=total_value)

            #update the users table
            db.execute("UPDATE users SET cash=:cash WHERE id=:user_id", cash=balance, user_id=user_id)

            return redirect("/")

        else:
            return apology("Cannot complete purchase not enough cash")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    user = db.execute("SELECT username FROM users WHERE username=:username", username=username)
    if not user:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # current user's user_id
    user_id = session["user_id"]

    # get all records from stock_trade_history for this user
    rows = db.execute("SELECT * FROM stock_trade_history WHERE user_id=:user_id", user_id=user_id)

    # render user stock history template
    return render_template("history.html", rows=rows)


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
    if request.method == "GET":
        return render_template("quote.html")
    if request.method == "POST":

        symbol = request.form.get("symbol")
        if symbol == "":
            return apology("please enter the stock code")

        stock_info = lookup(symbol)

        if not stock_info:
            return apology("stock code is invalid")
        else:
            return render_template("quoted.html", stock_info=stock_info)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        rows = db.execute("SELECT username FROM users WHERE username=:username", username=username)
        print(rows)

        if username == "":
            return apology("username is blank")
        if len(rows) == 1:
            return apology("user already exists")
        if password == "":
            return apology("password is blank")
        if confirmation == "":
            return apology("confirmation password is blank")
        if confirmation != password:
            return apology("passwords do not match")

        # hash the password
        pHash = generate_password_hash(password)

        # store data to new user
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :pHash)", username=username, pHash=pHash)

        return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("sell.html")

    if request.method == "POST":
        symbol = request.form.get("symbol")
        number_of_shares_string = request.form.get("number_of_shares")
        if symbol == "":
            return apology("symbol empty")
        if number_of_shares_string == "":
            return apology("number of shares empty")
        number_of_shares = int(number_of_shares_string)
        if number_of_shares < 1:
            return apology("enter a positive number for shares")

        user_id = session["user_id"]

        # if invalid stock code apologise
        stock_info = lookup(symbol)
        if not stock_info:
            return apology("stock code invalid")

        # if inadequate shares apologise
        available_shares = db.execute("SELECT number_of_shares FROM user_stock_info WHERE user_id=:user_id and symbol=:symbol", user_id=user_id, symbol=symbol)[0]["number_of_shares"]
        if available_shares < number_of_shares:
            return apology("Inadequate shares")

        # check if user owns the stock
        user_cash = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=user_id)[0]["cash"]
        rows = db.execute("SELECT symbol FROM user_stock_info WHERE user_id=:user_id and symbol=:symbol", user_id=user_id, symbol=symbol)
        if len(rows) > 0:
            # sell if true
            current_price = stock_info["price"]
            sell_value = current_price * number_of_shares
            user_cash += sell_value
            # update user's cash
            db.execute("UPDATE users SET cash=:cash WHERE id=:user_id", cash=user_cash, user_id=user_id)

            # update stock trade history
            db.execute("INSERT INTO stock_trade_history (user_id, symbol, price, buy_or_sell, number_of_shares, datetime) VALUES (:user_id, :symbol, :price, :buy_or_sell, :number_of_shares, :datetime)", user_id=user_id, symbol=symbol, price=current_price, buy_or_sell="Sold", number_of_shares=number_of_shares, datetime=datetime.now())

            # if final shares == 0 delete user stock info else update user stock info
            # delete stock info
            final_shares = available_shares - number_of_shares
            # delete the stock info record
            if final_shares == 0:
                db.execute("DELETE FROM user_stock_info WHERE user_id=:user_id and symbol=:symbol", user_id=user_id, symbol=symbol)
            #update stock info
            else:
                db.execute("UPDATE user_stock_info SET number_of_shares=:final_shares WHERE user_id=:user_id and symbol=:symbol", final_shares=final_shares, user_id=user_id, symbol=symbol)
            return redirect("/")
        # apology if false
        else:
            return apology("Buy the Stock first")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
