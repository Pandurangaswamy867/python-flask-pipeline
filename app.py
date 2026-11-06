
import os
import sqlite3
import secrets
from contextlib import contextmanager
from datetime import datetime
from functools import wraps

from flask import (
    Flask, request, redirect, url_for, session,
    flash, render_template_string, abort
)
from werkzeug.security import generate_password_hash, check_password_hash


# =====================================================
# APPLICATION CONFIGURATION
# =====================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY", "change-this-secret-key-for-your-demo"
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "data"))

os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "bubu_bank.db")

INITIAL_BALANCE = 10000000  # ₹1,00,000 in paise


# =====================================================
# DATABASE CONNECTION
# =====================================================

@contextmanager
def get_db():
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")

    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# =====================================================
# DATABASE INITIALIZATION
# =====================================================

def init_db():
    with get_db() as db:

        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                balance INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS holdings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                average_price INTEGER NOT NULL DEFAULT 0,
                UNIQUE(user_id, symbol),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                symbol TEXT,
                quantity INTEGER NOT NULL,
                price INTEGER NOT NULL,
                total INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symbol TEXT NOT NULL,
                UNIQUE(user_id, symbol),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)


init_db()


# =====================================================
# DEMO STOCK MARKET
# Prices are stored in paise, not rupees.
# These are simulated prices, NOT live market prices.
# =====================================================

MARKET = {
    "RELIANCE": {
        "name": "Reliance Industries",
        "price": 145000,
        "change": 1.25
    },
    "TCS": {
        "name": "Tata Consultancy Services",
        "price": 382000,
        "change": 0.85
    },
    "INFY": {
        "name": "Infosys",
        "price": 185000,
        "change": -0.45
    },
    "HDFCBANK": {
        "name": "HDFC Bank",
        "price": 168000,
        "change": 0.65
    },
    "ICICIBANK": {
        "name": "ICICI Bank",
        "price": 125000,
        "change": 1.10
    },
    "WIPRO": {
        "name": "Wipro",
        "price": 52000,
        "change": -0.35
    },
    "ITC": {
        "name": "ITC Limited",
        "price": 47000,
        "change": 0.55
    },
    "SBIN": {
        "name": "State Bank of India",
        "price": 82000,
        "change": 0.90
    },
    "TATAMOTORS": {
        "name": "Tata Motors",
        "price": 95000,
        "change": -1.20
    },
    "BHARTIARTL": {
        "name": "Bharti Airtel",
        "price": 178000,
        "change": 1.45
    }
}


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def money(amount):
    return f"₹{amount / 100:,.2f}"


def current_user():
    user_id = session.get("user_id")

    if not user_id:
        return None

    with get_db() as db:
        return db.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Please login to continue.", "error")
            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return wrapper


def csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(32)

    return session["_csrf_token"]


@app.before_request
def validate_csrf():
    if request.method == "POST":
        token = request.form.get("csrf_token", "")

        if not token or token != session.get("_csrf_token"):
            abort(400, description="Invalid security token. Refresh and try again.")


@app.context_processor
def inject_globals():
    return {
        "csrf_token": csrf_token,
        "money": money,
        "market": MARKET,
        "year": datetime.now().year
    }


# =====================================================
# AUTHENTICATION
# =====================================================

@app.route("/")
def index():
    if current_user():
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or len(password) < 8:
            flash("Enter your name, email and a password of at least 8 characters.", "error")
            return redirect(url_for("register"))

        try:
            with get_db() as db:
                db.execute("""
                    INSERT INTO users
                    (name, email, password, balance, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    name,
                    email,
                    generate_password_hash(password),
                    INITIAL_BALANCE,
                    datetime.now().isoformat(timespec="seconds")
                ))

            flash("Account created! Please login.", "success")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("This email is already registered.", "error")

    return render_template_string(TEMPLATE, page="register")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with get_db() as db:
            user = db.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            ).fetchone()

        if user and check_password_hash(user["password"], password):

            session.clear()
            session["user_id"] = user["id"]
            csrf_token()

            return redirect(url_for("dashboard"))

        flash("Incorrect email or password.", "error")

    return render_template_string(TEMPLATE, page="login")


@app.route("/logout", methods=["POST"])
@login_required
def logout():

    session.clear()
    flash("You have been logged out.", "success")

    return redirect(url_for("login"))


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
@login_required
def dashboard():

    user = current_user()

    with get_db() as db:

        holdings = db.execute("""
            SELECT * FROM holdings
            WHERE user_id = ? AND quantity > 0
        """, (user["id"],)).fetchall()

        transactions = db.execute("""
            SELECT * FROM transactions
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 5
        """, (user["id"],)).fetchall()

    portfolio_value = sum(
        h["quantity"] * MARKET[h["symbol"]]["price"]
        for h in holdings
        if h["symbol"] in MARKET
    )

    investment_cost = sum(
        h["quantity"] * h["average_price"]
        for h in holdings
    )

    profit_loss = portfolio_value - investment_cost

    return render_template_string(
        TEMPLATE,
        page="dashboard",
        user=user,
        holdings=holdings,
        transactions=transactions,
        portfolio_value=portfolio_value,
        profit_loss=profit_loss
    )


# =====================================================
# DEMO DEPOSIT
# =====================================================

@app.route("/deposit", methods=["POST"])
@login_required
def deposit():

    try:
        amount = float(request.form.get("amount", "0"))

        if not amount > 0 or amount > 100000:
            raise ValueError

        amount_paise = round(amount * 100)

        with get_db() as db:

            db.execute("""
                UPDATE users
                SET balance = balance + ?
                WHERE id = ?
            """, (amount_paise, session["user_id"]))

            db.execute("""
                INSERT INTO transactions
                (user_id, transaction_type, symbol, quantity,
                 price, total, created_at)
                VALUES (?, 'DEPOSIT', 'BANK', 1, ?, ?, ?)
            """, (
                session["user_id"],
                amount_paise,
                amount_paise,
                datetime.now().isoformat(timespec="seconds")
            ))

        flash("Demo deposit successful.", "success")

    except (ValueError, TypeError):
        flash("Enter a valid deposit amount.", "error")

    return redirect(url_for("dashboard"))


# =====================================================
# STOCK MARKET
# =====================================================

@app.route("/market")
@login_required
def stock_market():

    user = current_user()

    with get_db() as db:
        watchlist = db.execute("""
            SELECT symbol FROM watchlist
            WHERE user_id = ?
        """, (user["id"],)).fetchall()

    watch_symbols = [w["symbol"] for w in watchlist]

    return render_template_string(
        TEMPLATE,
        page="market",
        user=user,
        watch_symbols=watch_symbols
    )


# =====================================================
# BUY STOCK
# =====================================================

@app.route("/buy", methods=["POST"])
@login_required
def buy_stock():

    symbol = request.form.get("symbol", "").upper()

    try:
        quantity = int(request.form.get("quantity", "0"))
    except ValueError:
        quantity = 0

    if symbol not in MARKET or quantity < 1 or quantity > 100000:
        flash("Invalid stock or quantity.", "error")
        return redirect(url_for("stock_market"))

    price = MARKET[symbol]["price"]
    total = price * quantity
    user_id = session["user_id"]

    with get_db() as db:

        user = db.execute(
            "SELECT balance FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        if not user or user["balance"] < total:
            flash("Insufficient bank balance.", "error")
            return redirect(url_for("stock_market"))

        holding = db.execute("""
            SELECT * FROM holdings
            WHERE user_id = ? AND symbol = ?
        """, (user_id, symbol)).fetchone()

        if holding:

            old_quantity = holding["quantity"]
            new_quantity = old_quantity + quantity

            new_average = (
                old_quantity * holding["average_price"] + total
            ) // new_quantity

            db.execute("""
                UPDATE holdings
                SET quantity = ?, average_price = ?
                WHERE user_id = ? AND symbol = ?
            """, (
                new_quantity,
                new_average,
                user_id,
                symbol
            ))

        else:

            db.execute("""
                INSERT INTO holdings
                (user_id, symbol, quantity, average_price)
                VALUES (?, ?, ?, ?)
            """, (user_id, symbol, quantity, price))

        db.execute("""
            UPDATE users
            SET balance = balance - ?
            WHERE id = ?
        """, (total, user_id))

        db.execute("""
            INSERT INTO transactions
            (user_id, transaction_type, symbol, quantity,
             price, total, created_at)
            VALUES (?, 'BUY', ?, ?, ?, ?, ?)
        """, (
            user_id,
            symbol,
            quantity,
            price,
            total,
            datetime.now().isoformat(timespec="seconds")
        ))

    flash(f"Successfully bought {quantity} shares of {symbol}.", "success")

    return redirect(url_for("portfolio"))


# =====================================================
# SELL STOCK
# =====================================================

@app.route("/sell", methods=["POST"])
@login_required
def sell_stock():

    symbol = request.form.get("symbol", "").upper()

    try:
        quantity = int(request.form.get("quantity", "0"))
    except ValueError:
        quantity = 0

    if symbol not in MARKET or quantity < 1 or quantity > 100000:
        flash("Invalid stock or quantity.", "error")
        return redirect(url_for("portfolio"))

    user_id = session["user_id"]
    price = MARKET[symbol]["price"]
    total = price * quantity

    with get_db() as db:

        holding = db.execute("""
            SELECT * FROM holdings
            WHERE user_id = ? AND symbol = ?
        """, (user_id, symbol)).fetchone()

        if not holding or holding["quantity"] < quantity:
            flash("You do not have enough shares to sell.", "error")
            return redirect(url_for("portfolio"))

        remaining = holding["quantity"] - quantity

        if remaining == 0:
            db.execute("""
                DELETE FROM holdings
                WHERE user_id = ? AND symbol = ?
            """, (user_id, symbol))
        else:
            db.execute("""
                UPDATE holdings
                SET quantity = ?
                WHERE user_id = ? AND symbol = ?
            """, (remaining, user_id, symbol))

        db.execute("""
            UPDATE users
            SET balance = balance + ?
            WHERE id = ?
        """, (total, user_id))

        db.execute("""
            INSERT INTO transactions
            (user_id, transaction_type, symbol, quantity,
             price, total, created_at)
            VALUES (?, 'SELL', ?, ?, ?, ?, ?)
        """, (
            user_id,
            symbol,
            quantity,
            price,
            total,
            datetime.now().isoformat(timespec="seconds")
        ))

    flash(f"Successfully sold {quantity} shares of {symbol}.", "success")

    return redirect(url_for("portfolio"))


# =====================================================
# PORTFOLIO
# =====================================================

@app.route("/portfolio")
@login_required
def portfolio():

    user = current_user()

    with get_db() as db:
        holdings = db.execute("""
            SELECT * FROM holdings
            WHERE user_id = ? AND quantity > 0
        """, (user["id"],)).fetchall()

    portfolio_data = []
    total_value = 0
    total_cost = 0

    for holding in holdings:

        symbol = holding["symbol"]

        if symbol not in MARKET:
            continue

        market_price = MARKET[symbol]["price"]

        value = holding["quantity"] * market_price
        cost = holding["quantity"] * holding["average_price"]

        portfolio_data.append({
            "symbol": symbol,
            "name": MARKET[symbol]["name"],
            "quantity": holding["quantity"],
            "average_price": holding["average_price"],
            "market_price": market_price,
            "value": value,
            "profit_loss": value - cost
        })

        total_value += value
        total_cost += cost

    return render_template_string(
        TEMPLATE,
        page="portfolio",
        user=user,
        holdings=portfolio_data,
        total_value=total_value,
        total_cost=total_cost,
        profit_loss=total_value - total_cost
    )


# =====================================================
# WATCHLIST
# =====================================================

@app.route("/watchlist/add", methods=["POST"])
@login_required
def add_watchlist():

    symbol = request.form.get("symbol", "").upper()

    if symbol not in MARKET:
        flash("Invalid stock symbol.", "error")
        return redirect(url_for("stock_market"))

    try:
        with get_db() as db:
            db.execute("""
                INSERT INTO watchlist (user_id, symbol)
                VALUES (?, ?)
                ON CONFLICT(user_id, symbol) DO NOTHING
            """, (session["user_id"], symbol))

        flash(f"{symbol} added to your watchlist.", "success")

    except sqlite3.Error:
        flash("Unable to update watchlist.", "error")

    return redirect(url_for("stock_market"))


@app.route("/watchlist/remove", methods=["POST"])
@login_required
def remove_watchlist():

    symbol = request.form.get("symbol", "").upper()

    with get_db() as db:
        db.execute("""
            DELETE FROM watchlist
            WHERE user_id = ? AND symbol = ?
        """, (session["user_id"], symbol))

    flash("Stock removed from watchlist.", "success")

    return redirect(url_for("stock_market"))


# =====================================================
# TRANSACTION HISTORY
# =====================================================

@app.route("/transactions")
@login_required
def transaction_history():

    user = current_user()

    with get_db() as db:
        transactions = db.execute("""
            SELECT * FROM transactions
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user["id"],)).fetchall()

    return render_template_string(
        TEMPLATE,
        page="transactions",
        user=user,
        transactions=transactions
    )


# =====================================================
# HEALTH CHECK
# =====================================================

@app.route("/health")
def health():

    try:
        with get_db() as db:
            db.execute("SELECT 1")

        return {
            "status": "healthy",
            "database": "connected"
        }, 200

    except sqlite3.Error:
        return {
            "status": "unhealthy",
            "database": "error"
        }, 500


# =====================================================
# SINGLE-FILE HTML / CSS / JAVASCRIPT
# =====================================================

TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Bubu × Dudu Bank</title>

<style>

:root {
    --pink: #f6a6c8;
    --pink-dark: #e77eaa;
    --cream: #fff8f4;
    --brown: #624b55;
    --green: #238b68;
    --red: #d85a69;
    --white: #ffffff;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    background: var(--cream);
    color: var(--brown);
}

header {
    background: var(--white);
    padding: 18px 6%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 3px 15px #0000000a;
    flex-wrap: wrap;
    gap: 15px;
}

.logo {
    font-size: 23px;
    font-weight: bold;
    color: var(--pink-dark);
}

nav {
    display: flex;
    gap: 17px;
    flex-wrap: wrap;
    align-items: center;
}

nav a {
    text-decoration: none;
    color: var(--brown);
    font-size: 14px;
    font-weight: bold;
}

nav a:hover {
    color: var(--pink-dark);
}

.container {
    max-width: 1150px;
    margin: 35px auto;
    padding: 0 20px;
}

h1 {
    margin-bottom: 10px;
    font-size: 28px;
}

.subtitle {
    color: #987f8a;
    margin-bottom: 25px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 18px;
    margin: 25px 0;
}

.card {
    background: var(--white);
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 5px 20px #00000008;
}

.card h3 {
    font-size: 14px;
    color: #9b8290;
    margin-bottom: 15px;
}

.amount {
    font-size: 26px;
    font-weight: bold;
}

.pink {
    color: var(--pink-dark);
}

.green {
    color: var(--green);
}

.red {
    color: var(--red);
}

button, .button {
    background: var(--pink-dark);
    color: white;
    border: none;
    padding: 11px 17px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    text-decoration: none;
    display: inline-block;
}

button:hover, .button:hover {
    opacity: 0.85;
}

button.secondary {
    background: #eadde4;
    color: var(--brown);
}

button.danger {
    background: var(--red);
}

input {
    width: 100%;
    padding: 12px;
    border: 1px solid #eadde4;
    border-radius: 9px;
    margin: 8px 0 15px;
    font-size: 14px;
}

label {
    font-size: 13px;
    font-weight: bold;
}

form.inline {
    display: inline-block;
}

.table-wrap {
    overflow-x: auto;
    background: white;
    border-radius: 15px;
    margin-top: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
    min-width: 600px;
}

th, td {
    padding: 15px;
    border-bottom: 1px solid #f2e9ee;
    text-align: left;
    font-size: 14px;
}

th {
    color: #987f8a;
    background: #fffafd;
}

tr:last-child td {
    border-bottom: none;
}

.flash {
    padding: 13px 17px;
    border-radius: 10px;
    margin-bottom: 15px;
    background: #e6f7ef;
    color: #238b68;
}

.flash.error {
    background: #ffe9ed;
    color: #c13d55;
}

.auth {
    max-width: 420px;
    margin: 70px auto;
    padding: 30px;
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 35px #0000000c;
}

.auth h1 {
    text-align: center;
    color: var(--pink-dark);
}

.auth p {
    text-align: center;
    margin: 15px 0 25px;
    color: #987f8a;
}

.auth button {
    width: 100%;
}

.auth a {
    color: var(--pink-dark);
}

.actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
}

.stock-symbol {
    font-weight: bold;
}

.small {
    font-size: 12px;
    color: #987f8a;
}

footer {
    text-align: center;
    padding: 30px;
    color: #987f8a;
    font-size: 12px;
}

@media(max-width: 650px) {
    header {
        align-items: flex-start;
        flex-direction: column;
    }

    nav {
        gap: 12px;
    }

    h1 {
        font-size: 23px;
    }

    .container {
        margin-top: 25px;
    }
}

</style>
</head>

<body>

{% if page not in ['login', 'register'] %}

<header>

    <div class="logo">🐻 Bubu × Dudu Bank 🐼</div>

    <nav>
        <a href="{{ url_for('dashboard') }}">Dashboard</a>
        <a href="{{ url_for('stock_market') }}">Market</a>
        <a href="{{ url_for('portfolio') }}">Portfolio</a>
        <a href="{{ url_for('transaction_history') }}">Transactions</a>

        <form method="POST" action="{{ url_for('logout') }}" class="inline">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <button class="secondary">Logout</button>
        </form>
    </nav>

</header>

{% endif %}


{% if page in ['login', 'register'] %}

<div class="auth">

    <h1>🐻 Bubu × Dudu 🐼</h1>
    <p>Banking and Trading Universe</p>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}
            <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
    {% endwith %}

    {% if page == 'login' %}

        <form method="POST">

            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

            <label>Email address</label>
            <input type="email" name="email" placeholder="Enter your email" required>

            <label>Password</label>
            <input type="password" name="password" placeholder="Enter password" required>

            <button type="submit">Login to your account</button>

        </form>

        <p>Don't have an account?
            <a href="{{ url_for('register') }}">Register here</a>
        </p>

    {% else %}

        <form method="POST">

            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

            <label>Your name</label>
            <input type="text" name="name" placeholder="Your name" required>

            <label>Email address</label>
            <input type="email" name="email" placeholder="Your email" required>

            <label>Password (minimum 8 characters)</label>
            <input type="password" name="password" minlength="8" required>

            <button type="submit">Create account</button>

        </form>

        <p>Already registered?
            <a href="{{ url_for('login') }}">Login here</a>
        </p>

    {% endif %}

</div>


{% elif page == 'dashboard' %}

<div class="container">

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}
            <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
    {% endwith %}

    <h1>Hello, {{ user.name }}! 💗</h1>
    <p class="subtitle">Welcome to your Bubu × Dudu financial universe.</p>

    <div class="grid">

        <div class="card">
            <h3>AVAILABLE BANK BALANCE</h3>
            <div class="amount">{{ money(user.balance) }}</div>
        </div>

        <div class="card">
            <h3>STOCK PORTFOLIO VALUE</h3>
            <div class="amount pink">{{ money(portfolio_value) }}</div>
        </div>

        <div class="card">
            <h3>INVESTMENT UNREALIZED P/L</h3>
            <div class="amount {{ 'green' if profit_loss >= 0 else 'red' }}">
                {{ money(profit_loss) }}
            </div>
        </div>

    </div>

    <div class="grid">

        <div class="card">

            <h3>ADD DEMO MONEY</h3>

            <form method="POST" action="{{ url_for('deposit') }}">

                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

                <label>Deposit amount (₹)</label>
                <input type="number" name="amount" min="1" max="100000"
                       step="0.01" placeholder="Enter amount" required>

                <button type="submit">Add demo money</button>

            </form>

            <p class="small">This is simulated money, not a real bank transfer.</p>

        </div>

        <div class="card">

            <h3>QUICK ACTIONS</h3>

            <div class="actions">
                <a class="button" href="{{ url_for('stock_market') }}">Explore stocks</a>
                <a class="button" href="{{ url_for('portfolio') }}">My portfolio</a>
            </div>

        </div>

    </div>

    <h2>My Holdings</h2>

    <div class="table-wrap">
        <table>
            <tr>
                <th>Stock</th>
                <th>Quantity</th>
                <th>Average Price</th>
                <th>Current Value</th>
            </tr>

            {% for h in holdings %}
            <tr>
                <td>{{ h.symbol }}</td>
                <td>{{ h.quantity }}</td>
                <td>{{ money(h.average_price) }}</td>
                <td>{{ money(h.quantity * market[h.symbol].price) }}</td>
            </tr>
            {% else %}
            <tr><td colspan="4">No stocks purchased yet.</td></tr>
            {% endfor %}

        </table>
    </div>

    <h2 style="margin-top:30px">Recent Transactions</h2>

    <div class="table-wrap">
        <table>
            <tr>
                <th>Type</th>
                <th>Stock</th>
                <th>Quantity</th>
                <th>Total</th>
                <th>Date</th>
            </tr>

            {% for t in transactions %}
            <tr>
                <td>{{ t.transaction_type }}</td>
                <td>{{ t.symbol }}</td>
                <td>{{ t.quantity }}</td>
                <td>{{ money(t.total) }}</td>
                <td>{{ t.created_at }}</td>
            </tr>
            {% else %}
            <tr><td colspan="5">No transactions yet.</td></tr>
            {% endfor %}

        </table>
    </div>

</div>


{% elif page == 'market' %}

<div class="container">

    <h1>📈 Stock Market</h1>
    <p class="subtitle">Explore stocks and make simulated trades.</p>

    <div class="card">
        <h3>AVAILABLE BALANCE</h3>
        <div class="amount">{{ money(user.balance) }}</div>
    </div>

    <div class="table-wrap">

        <table>

            <tr>
                <th>Company</th>
                <th>Symbol</th>
                <th>Price</th>
                <th>Change</th>
                <th>Buy</th>
                <th>Watchlist</th>
            </tr>

            {% for symbol, stock in market.items() %}

            <tr>

                <td>{{ stock.name }}</td>

                <td class="stock-symbol">{{ symbol }}</td>

                <td>{{ money(stock.price) }}</td>

                <td class="{{ 'green' if stock.change >= 0 else 'red' }}">
                    {{ stock.change }}%
                </td>

                <td>

                    <form method="POST" action="{{ url_for('buy_stock') }}">

                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                        <input type="hidden" name="symbol" value="{{ symbol }}">

                        <input type="number" name="quantity" min="1"
                               max="100000" value="1" required
                               style="width:65px;margin:0">

                        <button type="submit">Buy</button>

                    </form>

                </td>

                <td>

                    {% if symbol in watch_symbols %}

                    <form method="POST" action="{{ url_for('remove_watchlist') }}">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                        <input type="hidden" name="symbol" value="{{ symbol }}">
                        <button class="secondary">Remove</button>
                    </form>

                    {% else %}

                    <form method="POST" action="{{ url_for('add_watchlist') }}">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                        <input type="hidden" name="symbol" value="{{ symbol }}">
                        <button class="secondary">+ Watch</button>
                    </form>

                    {% endif %}

                </td>

            </tr>

            {% endfor %}

        </table>

    </div>

    <p class="small" style="margin-top:15px">
        Prices are simulated demonstration values. They are not live NSE or BSE prices.
    </p>

</div>


{% elif page == 'portfolio' %}

<div class="container">

    <h1>💼 My Portfolio</h1>
    <p class="subtitle">Track your stock investments.</p>

    <div class="grid">

        <div class="card">
            <h3>PORTFOLIO VALUE</h3>
            <div class="amount">{{ money(total_value) }}</div>
        </div>

        <div class="card">
            <h3>INVESTED AMOUNT</h3>
            <div class="amount">{{ money(total_cost) }}</div>
        </div>

        <div class="card">
            <h3>UNREALIZED PROFIT / LOSS</h3>
            <div class="amount {{ 'green' if profit_loss >= 0 else 'red' }}">
                {{ money(profit_loss) }}
            </div>
        </div>

    </div>

    <div class="table-wrap">

        <table>

            <tr>
                <th>Stock</th>
                <th>Quantity</th>
                <th>Average Price</th>
                <th>Market Price</th>
                <th>Current Value</th>
                <th>P/L</th>
                <th>Sell</th>
            </tr>

            {% for h in holdings %}

            <tr>

                <td>{{ h.name }} ({{ h.symbol }})</td>
                <td>{{ h.quantity }}</td>
                <td>{{ money(h.average_price) }}</td>
                <td>{{ money(h.market_price) }}</td>
                <td>{{ money(h.value) }}</td>

                <td class="{{ 'green' if h.profit_loss >= 0 else 'red' }}">
                    {{ money(h.profit_loss) }}
                </td>

                <td>

                    <form method="POST" action="{{ url_for('sell_stock') }}">

                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                        <input type="hidden" name="symbol" value="{{ h.symbol }}">

                        <input type="number" name="quantity" min="1"
                               max="{{ h.quantity }}" value="1"
                               required style="width:65px;margin:0">

                        <button class="danger" type="submit">Sell</button>

                    </form>

                </td>

            </tr>

            {% else %}

            <tr><td colspan="7">Your portfolio is empty. Visit the market to buy stocks.</td></tr>

            {% endfor %}

        </table>

    </div>

</div>


{% elif page == 'transactions' %}

<div class="container">

    <h1>📋 Transaction History</h1>
    <p class="subtitle">All your banking and trading activity.</p>

    <div class="table-wrap">

        <table>

            <tr>
                <th>Type</th>
                <th>Symbol</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total</th>
                <th>Date</th>
            </tr>

            {% for t in transactions %}

            <tr>
                <td>{{ t.transaction_type }}</td>
                <td>{{ t.symbol }}</td>
                <td>{{ t.quantity }}</td>
                <td>{{ money(t.price) }}</td>
                <td>{{ money(t.total) }}</td>
                <td>{{ t.created_at }}</td>
            </tr>

            {% else %}

            <tr><td colspan="6">No transactions found.</td></tr>

            {% endfor %}

        </table>

    </div>

</div>

{% endif %}


<footer>
    Bubu × Dudu Bank & Trading Universe © {{ year }}
    <br>
    Educational simulation only. No real money or securities are involved.
</footer>

</body>
</html>
"""


# =====================================================
# START APPLICATION
# =====================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
