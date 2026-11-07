#Hello dudu this is bubu how are you 
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
<meta name="theme-color" content="#101c2c">
<title>{% if page == 'login' %}Sign in{% elif page == 'register' %}Create account{% else %}{{ page|title }}{% endif %} · Bubu Finance</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --navy: #101c2c;
  --navy-2: #17283d;
  --navy-3: #243a52;
  --ink: #182536;
  --muted: #788697;
  --line: #e8edf2;
  --canvas: #f4f7fa;
  --surface: #ffffff;
  --teal: #12a889;
  --teal-dark: #07866d;
  --teal-soft: #e5f7f2;
  --green: #16865f;
  --green-soft: #e7f6ef;
  --red: #d95763;
  --red-soft: #fff0f1;
  --amber: #b7791f;
  --shadow: 0 8px 28px rgba(21, 39, 58, .055);
  --radius: 16px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; background: var(--canvas); color: var(--ink);
  font-family: 'DM Sans', Arial, sans-serif; font-size: 14px;
  -webkit-font-smoothing: antialiased;
}
button, input { font: inherit; }
a { color: inherit; }
.app-shell { min-height: 100vh; }
.sidebar {
  width: 248px; position: fixed; inset: 0 auto 0 0; z-index: 20;
  background: var(--navy); color: #d6e0ea; padding: 26px 17px;
  display: flex; flex-direction: column;
}
.brand { display: flex; align-items: center; gap: 11px; padding: 0 10px 32px; }
.brand-mark {
  width: 39px; height: 39px; display: grid; place-items: center;
  background: linear-gradient(145deg, #20c6a1, #087e70); color: white;
  border-radius: 12px; font-size: 19px; box-shadow: 0 7px 18px #0aa88935;
}
.brand-name { font: 800 17px 'Manrope', sans-serif; color: #fff; letter-spacing: -.5px; }
.brand-sub { color: #8294a8; font-size: 10px; margin-top: 2px; letter-spacing: 1.3px; text-transform: uppercase; }
.nav-label { color: #71859a; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; padding: 12px 12px 9px; text-transform: uppercase; }
.nav-list { display: grid; gap: 5px; }
.nav-link {
  display: flex; align-items: center; gap: 13px; padding: 12px 13px;
  color: #aebdcb; text-decoration: none; border-radius: 10px;
  font-size: 13px; font-weight: 600; transition: .18s ease;
}
.nav-link:hover { background: #ffffff0c; color: #fff; }
.nav-link.active { color: #fff; background: linear-gradient(90deg, #0da88935, #0da88912); box-shadow: inset 3px 0 #19c5a0; }
.nav-icon { width: 19px; text-align: center; font-size: 16px; opacity: .95; }
.sidebar-bottom { margin-top: auto; }
.demo-note {
  border: 1px solid #ffffff17; border-radius: 12px; padding: 13px;
  color: #9fb0c1; font-size: 11px; line-height: 1.6; background: #ffffff08;
}
.demo-note strong { display: block; color: #e4edf5; font-size: 12px; margin-bottom: 3px; }
.main-area { margin-left: 248px; min-height: 100vh; }
.topbar {
  height: 76px; background: #fff; border-bottom: 1px solid var(--line);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 38px; position: sticky; top: 0; z-index: 10;
}
.breadcrumb { color: var(--muted); font-size: 12px; }
.breadcrumb strong { color: var(--ink); font-weight: 700; }
.top-actions { display: flex; align-items: center; gap: 18px; }
.live-pill { display: inline-flex; align-items: center; gap: 7px; color: #16865f; background: var(--green-soft); border-radius: 30px; padding: 7px 11px; font-size: 11px; font-weight: 700; }
.live-dot { width: 6px; height: 6px; border-radius: 50%; background: #20ad78; box-shadow: 0 0 0 3px #20ad7820; }
.profile { display: flex; align-items: center; gap: 10px; }
.avatar { width: 36px; height: 36px; border-radius: 50%; background: #e4f4ef; color: #07866d; display: grid; place-items: center; font-weight: 800; }
.profile-name { font-size: 12px; font-weight: 700; }
.profile-caption { color: var(--muted); font-size: 10px; margin-top: 2px; }
.page-wrap { max-width: 1440px; margin: auto; padding: 34px 38px 50px; }
.page-heading { display: flex; justify-content: space-between; align-items: flex-start; gap: 20px; margin-bottom: 26px; }
h1 { font: 800 25px 'Manrope', sans-serif; letter-spacing: -.8px; margin: 0 0 7px; color: #172638; }
h2 { font: 750 16px 'Manrope', sans-serif; margin: 0; color: #1c2c3e; }
.subtitle { color: var(--muted); font-size: 12px; margin: 0; }
.eyebrow { color: var(--teal-dark); font-size: 10px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 9px; }
.grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 17px; margin-bottom: 20px; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 21px; box-shadow: var(--shadow); min-width: 0; }
.metric-card { position: relative; overflow: hidden; }
.metric-top { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.metric-label { color: #7d8a99; font-size: 10px; font-weight: 800; letter-spacing: 1.1px; text-transform: uppercase; }
.metric-icon { width: 34px; height: 34px; display: grid; place-items: center; border-radius: 10px; background: var(--teal-soft); color: var(--teal-dark); font-size: 16px; }
.metric-value { font: 800 25px 'Manrope', sans-serif; letter-spacing: -.8px; margin: 15px 0 7px; color: #172638; }
.metric-foot { color: var(--muted); font-size: 11px; }
.metric-foot strong { color: var(--green); }
.positive { color: var(--green) !important; }
.negative { color: var(--red) !important; }
.pill { display: inline-flex; align-items: center; border-radius: 30px; padding: 5px 9px; font-size: 10px; font-weight: 800; background: var(--green-soft); color: var(--green); }
.pill.down { background: var(--red-soft); color: var(--red); }
.hero-card {
  background: linear-gradient(120deg, #14263b 0%, #1b4052 100%);
  color: white; border: 0; position: relative; overflow: hidden;
}
.hero-card:after { content: ""; position: absolute; width: 240px; height: 240px; border: 1px solid #ffffff16; border-radius: 50%; right: -55px; top: -105px; box-shadow: 0 0 0 28px #ffffff08, 0 0 0 58px #ffffff05; }
.hero-card .metric-label, .hero-card .metric-foot { color: #b7c8d4; }
.hero-card .metric-value { color: white; font-size: 31px; }
.hero-card .metric-icon { background: #ffffff18; color: #72e0c4; }
.section-head { display: flex; align-items: center; justify-content: space-between; gap: 14px; margin-bottom: 17px; }
.section-link { color: var(--teal-dark); font-size: 11px; font-weight: 800; text-decoration: none; }
.content-grid { display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(260px, .9fr); gap: 18px; margin-bottom: 20px; }
.table-wrap { overflow-x: auto; width: 100%; }
table { width: 100%; border-collapse: collapse; min-width: 570px; }
th { text-align: left; padding: 12px 13px; color: #8a97a5; background: #f8fafc; font-size: 9px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; white-space: nowrap; }
td { padding: 14px 13px; border-bottom: 1px solid #edf1f5; color: #405064; font-size: 12px; white-space: nowrap; }
tr:last-child td { border-bottom: 0; }
tbody tr:hover { background: #fbfdfd; }
.stock-cell { display: flex; align-items: center; gap: 10px; }
.stock-badge { width: 30px; height: 30px; border-radius: 9px; background: #edf4f7; color: #31556a; display: grid; place-items: center; font-size: 10px; font-weight: 800; }
.stock-name { font-weight: 700; color: #26384b; }
.stock-symbol { font-size: 10px; color: #8b98a6; margin-top: 3px; }
.muted { color: var(--muted); }
.btn {
  border: 0; border-radius: 9px; padding: 10px 15px; display: inline-flex;
  justify-content: center; align-items: center; gap: 7px; cursor: pointer;
  text-decoration: none; font-size: 11px; font-weight: 800; transition: .18s ease;
}
.btn-primary { background: var(--teal); color: white; box-shadow: 0 5px 12px #12a88925; }
.btn-primary:hover { background: var(--teal-dark); transform: translateY(-1px); }
.btn-light { background: #eef3f6; color: #42566a; }
.btn-light:hover { background: #e2eaef; }
.btn-danger { background: var(--red-soft); color: var(--red); }
.btn-danger:hover { background: #ffe2e5; }
.btn-small { padding: 7px 10px; font-size: 10px; }
.inline-form { display: inline-flex; align-items: center; gap: 6px; }
input {
  width: 100%; border: 1px solid #dfe6ec; background: #fbfcfd;
  border-radius: 9px; padding: 11px 12px; color: var(--ink);
  outline: none; transition: .18s ease;
}
input:focus { border-color: #37b99e; background: white; box-shadow: 0 0 0 3px #12a88915; }
input[type=number].qty { width: 65px; padding: 8px 7px; }
label { display: block; color: #536477; font-size: 11px; font-weight: 700; margin: 0 0 7px; }
.field { margin-bottom: 15px; }
.flash { padding: 12px 15px; border-radius: 10px; margin-bottom: 16px; font-size: 12px; font-weight: 600; border: 1px solid #ccebdd; color: #137a58; background: #effaf5; }
.flash.error { border-color: #f6d2d6; color: #bd4351; background: #fff4f5; }
.deposit-form { display: flex; gap: 9px; align-items: end; }
.deposit-form .field { flex: 1; margin: 0; }
.deposit-form input { min-width: 0; }
.quick-actions { display: flex; flex-wrap: wrap; gap: 9px; margin-top: 16px; }
.empty { padding: 28px 15px; text-align: center; color: #8996a4; font-size: 12px; }
.auth-page {
  min-height: 100vh; display: grid; grid-template-columns: 1.05fr .95fr;
  background: #f4f7fa;
}
.auth-visual {
  background: radial-gradient(circle at 20% 15%, #24566a 0, transparent 35%),
              linear-gradient(145deg, #101c2c, #19394b);
  color: white; padding: 8vw; display: flex; flex-direction: column; justify-content: space-between;
  position: relative; overflow: hidden;
}
.auth-visual:after { content: ""; position: absolute; width: 500px; height: 500px; border: 1px solid #ffffff18; border-radius: 50%; right: -170px; bottom: -190px; box-shadow: 0 0 0 45px #ffffff08, 0 0 0 90px #ffffff05; }
.auth-visual .brand { padding: 0; position: relative; z-index: 1; }
.auth-copy { max-width: 520px; position: relative; z-index: 1; }
.auth-copy h2 { color: white; font: 800 clamp(32px, 4vw, 54px) 'Manrope', sans-serif; line-height: 1.12; letter-spacing: -2px; margin: 0 0 18px; }
.auth-copy p { color: #b7c8d4; font-size: 14px; line-height: 1.8; max-width: 410px; }
.auth-stats { display: flex; gap: 35px; margin-top: 38px; }
.auth-stat strong { display: block; font: 800 20px 'Manrope', sans-serif; color: #72e0c4; }
.auth-stat span { color: #9fb2c2; font-size: 10px; }
.auth-footer { color: #8298aa; font-size: 10px; position: relative; z-index: 1; }
.auth-panel { display: grid; place-items: center; padding: 35px 24px; }
.auth-box { width: 100%; max-width: 410px; background: white; border: 1px solid var(--line); border-radius: 20px; padding: 36px; box-shadow: 0 18px 55px #17283d0c; }
.auth-box h1 { font-size: 25px; margin-bottom: 8px; }
.auth-box .subtitle { margin-bottom: 28px; line-height: 1.6; }
.auth-box .btn { width: 100%; padding: 13px; margin-top: 5px; }
.auth-switch { text-align: center; color: var(--muted); font-size: 11px; margin-top: 23px; }
.auth-switch a { color: var(--teal-dark); font-weight: 800; text-decoration: none; }
.security-note { background: #f4f8fa; border-radius: 9px; padding: 11px; margin-top: 18px; color: #7d8b99; font-size: 10px; line-height: 1.5; }
.footer { text-align: center; color: #98a4b0; font-size: 10px; padding: 28px 10px; }
.notice { color: #8b6b2c; background: #fff8e8; border: 1px solid #f2e5c5; padding: 11px 13px; border-radius: 9px; font-size: 11px; line-height: 1.6; margin-top: 15px; }
.balance-large { font: 800 22px 'Manrope', sans-serif; color: #172638; margin-top: 8px; }
@media (max-width: 1050px) {
  .sidebar { width: 210px; }
  .main-area { margin-left: 210px; }
  .page-wrap { padding: 28px 24px 40px; }
  .topbar { padding: 0 24px; }
  .content-grid { grid-template-columns: 1fr; }
}
@media (max-width: 760px) {
  .sidebar { position: static; width: 100%; padding: 13px 15px; }
  .brand { padding: 0 4px 12px; }
  .nav-label, .sidebar-bottom { display: none; }
  .nav-list { display: flex; overflow-x: auto; gap: 5px; padding-bottom: 2px; }
  .nav-link { flex: 0 0 auto; padding: 9px 11px; font-size: 11px; }
  .nav-icon { display: none; }
  .main-area { margin-left: 0; }
  .topbar { height: 58px; padding: 0 17px; }
  .page-wrap { padding: 24px 16px 35px; }
  .grid { grid-template-columns: 1fr; gap: 11px; }
  .page-heading { flex-direction: column; }
  .auth-page { grid-template-columns: 1fr; }
  .auth-visual { display: none; }
  .auth-panel { min-height: 100vh; padding: 20px; }
  .auth-box { padding: 27px 22px; }
  .deposit-form { align-items: stretch; flex-direction: column; }
}
</style>
</head>
<body>

{% if page in ['login', 'register'] %}
<div class="auth-page">
  <section class="auth-visual">
    <div class="brand">
      <div class="brand-mark">B</div>
      <div><div class="brand-name">Bubu Finance</div><div class="brand-sub">Banking · Investing · Growing</div></div>
    </div>
    <div class="auth-copy">
      <div class="eyebrow" style="color:#72e0c4">YOUR MONEY, YOUR MOVES</div>
      <h2>A smarter way to explore your financial world.</h2>
      <p>Manage your demo balance, explore the market, and understand your portfolio from one clean dashboard.</p>
      <div class="auth-stats">
        <div class="auth-stat"><strong>01</strong><span>Banking overview</span></div>
        <div class="auth-stat"><strong>02</strong><span>Market simulator</span></div>
        <div class="auth-stat"><strong>03</strong><span>Portfolio insights</span></div>
      </div>
    </div>
    <div class="auth-footer">Bubu Finance · Educational trading simulator</div>
  </section>
  <section class="auth-panel">
    <div class="auth-box">
      <div class="eyebrow">WELCOME TO BUBU FINANCE</div>
      {% if page == 'login' %}
        <h1>Sign in to your account</h1>
        <p class="subtitle">Enter your details to access your financial dashboard.</p>
      {% else %}
        <h1>Create your account</h1>
        <p class="subtitle">Set up your demo account and start exploring.</p>
      {% endif %}
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}<div class="flash {{ category }}">{{ message }}</div>{% endfor %}
      {% endwith %}
      {% if page == 'login' %}
      <form method="POST">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <div class="field"><label>Email address</label><input type="email" name="email" placeholder="you@example.com" autocomplete="email" required></div>
        <div class="field"><label>Password</label><input type="password" name="password" placeholder="Enter your password" autocomplete="current-password" required></div>
        <button class="btn btn-primary" type="submit">Sign in securely →</button>
      </form>
      <div class="auth-switch">New to Bubu Finance? <a href="{{ url_for('register') }}">Create an account</a></div>
      {% else %}
      <form method="POST">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <div class="field"><label>Full name</label><input type="text" name="name" placeholder="Your name" autocomplete="name" required></div>
        <div class="field"><label>Email address</label><input type="email" name="email" placeholder="you@example.com" autocomplete="email" required></div>
        <div class="field"><label>Password</label><input type="password" name="password" minlength="8" placeholder="At least 8 characters" autocomplete="new-password" required></div>
        <button class="btn btn-primary" type="submit">Create demo account →</button>
      </form>
      <div class="auth-switch">Already registered? <a href="{{ url_for('login') }}">Sign in</a></div>
      {% endif %}
      <div class="security-note">🔒 Demo environment. Do not use a real banking password or sensitive financial information.</div>
    </div>
  </section>
</div>

{% else %}
<div class="app-shell">
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-mark">B</div>
      <div><div class="brand-name">Bubu Finance</div><div class="brand-sub">Personal wealth</div></div>
    </div>
    <div class="nav-label">Workspace</div>
    <nav class="nav-list">
      <a class="nav-link {{ 'active' if page == 'dashboard' else '' }}" href="{{ url_for('dashboard') }}"><span class="nav-icon">▦</span>Overview</a>
      <a class="nav-link {{ 'active' if page == 'market' else '' }}" href="{{ url_for('stock_market') }}"><span class="nav-icon">⌁</span>Market</a>
      <a class="nav-link {{ 'active' if page == 'portfolio' else '' }}" href="{{ url_for('portfolio') }}"><span class="nav-icon">◫</span>My portfolio</a>
      <a class="nav-link {{ 'active' if page == 'transactions' else '' }}" href="{{ url_for('transaction_history') }}"><span class="nav-icon">↔</span>Transactions</a>
    </nav>
    <div class="sidebar-bottom">
      <div class="demo-note"><strong>Demo account</strong>All balances, deposits and trades are simulated. No real funds or securities are involved.</div>
    </div>
  </aside>

  <main class="main-area">
    <header class="topbar">
      <div class="breadcrumb">Workspace <span style="padding:0 7px;color:#c1cbd4">/</span> <strong>{{ {'dashboard':'Overview','market':'Market','portfolio':'My portfolio','transactions':'Transactions'}.get(page, page|title) }}</strong></div>
      <div class="top-actions">
        <span class="live-pill"><span class="live-dot"></span> Simulation active</span>
        <div class="profile">
          <div class="avatar">{{ user.name[:1]|upper }}</div>
          <div><div class="profile-name">{{ user.name }}</div><div class="profile-caption">Demo account</div></div>
        </div>
        <form method="POST" action="{{ url_for('logout') }}">
          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
          <button class="btn btn-light btn-small" type="submit">Sign out</button>
        </form>
      </div>
    </header>

    <div class="page-wrap">
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}<div class="flash {{ category }}">{{ message }}</div>{% endfor %}
      {% endwith %}

      {% if page == 'dashboard' %}
      <div class="page-heading">
        <div><div class="eyebrow">ACCOUNT OVERVIEW</div><h1>Good to see you, {{ user.name }}.</h1><p class="subtitle">Here's what's happening with your demo finances today.</p></div>
        <span class="pill">● Account active</span>
      </div>

      <div class="grid">
        <div class="card metric-card hero-card">
          <div class="metric-top"><span class="metric-label">Available cash balance</span><span class="metric-icon">₹</span></div>
          <div class="metric-value">{{ money(user.balance) }}</div>
          <div class="metric-foot">Ready to use for simulated trades</div>
        </div>
        <div class="card metric-card">
          <div class="metric-top"><span class="metric-label">Portfolio market value</span><span class="metric-icon">◫</span></div>
          <div class="metric-value">{{ money(portfolio_value) }}</div>
          <div class="metric-foot">Current value of your open positions</div>
        </div>
        <div class="card metric-card">
          <div class="metric-top"><span class="metric-label">Unrealized profit / loss</span><span class="metric-icon">↗</span></div>
          <div class="metric-value {{ 'positive' if profit_loss >= 0 else 'negative' }}">{{ money(profit_loss) }}</div>
          <div class="metric-foot">{% if profit_loss >= 0 %}Above{% else %}Below{% endif %} your average purchase cost</div>
        </div>
      </div>

      <div class="content-grid">
        <section class="card">
          <div class="section-head"><div><h2>Portfolio holdings</h2><p class="subtitle" style="margin-top:5px">A snapshot of your open positions</p></div><a class="section-link" href="{{ url_for('portfolio') }}">View portfolio →</a></div>
          <div class="table-wrap"><table>
            <thead><tr><th>Asset</th><th>Units</th><th>Avg. cost</th><th>Market value</th></tr></thead>
            <tbody>
            {% for h in holdings %}
            <tr><td><div class="stock-cell"><div class="stock-badge">{{ h.symbol[:2] }}</div><div><div class="stock-name">{{ market[h.symbol].name }}</div><div class="stock-symbol">{{ h.symbol }}</div></div></div></td><td>{{ h.quantity }}</td><td>{{ money(h.average_price) }}</td><td style="font-weight:700;color:#26384b">{{ money(h.quantity * market[h.symbol].price) }}</td></tr>
            {% else %}<tr><td colspan="4" class="empty">No holdings yet. Explore the market to make your first simulated trade.</td></tr>{% endfor %}
            </tbody>
          </table></div>
        </section>
        <section class="card">
          <div class="section-head"><div><h2>Add demo funds</h2><p class="subtitle" style="margin-top:5px">Top up your simulated cash balance</p></div><span class="metric-icon">＋</span></div>
          <form method="POST" action="{{ url_for('deposit') }}">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <div class="field"><label>Amount in INR</label><input type="number" name="amount" min="1" max="100000" step="0.01" placeholder="e.g. 5000" required></div>
            <button class="btn btn-primary" type="submit">Add demo funds →</button>
          </form>
          <div class="notice">This action creates simulated funds only. It does not connect to a bank or payment gateway.</div>
          <div class="quick-actions"><a class="btn btn-light" href="{{ url_for('stock_market') }}">Explore market</a><a class="btn btn-light" href="{{ url_for('transaction_history') }}">Activity history</a></div>
        </section>
      </div>

      <section class="card">
        <div class="section-head"><div><h2>Recent activity</h2><p class="subtitle" style="margin-top:5px">Your latest account transactions</p></div><a class="section-link" href="{{ url_for('transaction_history') }}">All transactions →</a></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Type</th><th>Asset</th><th>Quantity</th><th>Total value</th><th>Timestamp</th></tr></thead>
          <tbody>{% for t in transactions %}
          <tr><td><span class="pill {{ 'down' if t.transaction_type == 'BUY' else '' }}">{{ t.transaction_type }}</span></td><td>{{ t.symbol }}</td><td>{{ t.quantity }}</td><td style="font-weight:700">{{ money(t.total) }}</td><td class="muted">{{ t.created_at }}</td></tr>
          {% else %}<tr><td colspan="5" class="empty">No activity to display.</td></tr>{% endfor %}</tbody>
        </table></div>
      </section>

      {% elif page == 'market' %}
      <div class="page-heading"><div><div class="eyebrow">INVESTMENT EXPLORER</div><h1>Market watch</h1><p class="subtitle">Browse available instruments and place simulated orders.</p></div><div class="card" style="padding:12px 16px"><div class="metric-label">AVAILABLE CASH</div><div class="balance-large">{{ money(user.balance) }}</div></div></div>
      <section class="card">
        <div class="section-head"><div><h2>Available instruments</h2><p class="subtitle" style="margin-top:5px">Prices shown are fixed demo values</p></div><span class="pill">10 instruments</span></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Company</th><th>Symbol</th><th>Demo price</th><th>Change</th><th>Order quantity</th><th>Watchlist</th></tr></thead>
          <tbody>{% for symbol, stock in market.items() %}
          <tr>
            <td><div class="stock-cell"><div class="stock-badge">{{ symbol[:2] }}</div><div class="stock-name">{{ stock.name }}</div></div></td>
            <td><strong>{{ symbol }}</strong></td><td style="font-weight:700">{{ money(stock.price) }}</td>
            <td><span class="pill {{ 'down' if stock.change < 0 else '' }}">{{ '+' if stock.change > 0 else '' }}{{ stock.change }}%</span></td>
            <td><form class="inline-form" method="POST" action="{{ url_for('buy_stock') }}"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}"><input type="hidden" name="symbol" value="{{ symbol }}"><input class="qty" type="number" name="quantity" min="1" max="100000" value="1" required><button class="btn btn-primary btn-small" type="submit">Buy</button></form></td>
            <td>{% if symbol in watch_symbols %}
              <form method="POST" action="{{ url_for('remove_watchlist') }}"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}"><input type="hidden" name="symbol" value="{{ symbol }}"><button class="btn btn-light btn-small" type="submit">Remove</button></form>
            {% else %}
              <form method="POST" action="{{ url_for('add_watchlist') }}"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}"><input type="hidden" name="symbol" value="{{ symbol }}"><button class="btn btn-light btn-small" type="submit">＋ Watch</button></form>
            {% endif %}</td>
          </tr>{% endfor %}</tbody>
        </table></div>
        <div class="notice">Market prices and percentage changes are illustrative placeholders, not live NSE/BSE quotes. Orders are not routed to an exchange.</div>
      </section>

      {% elif page == 'portfolio' %}
      <div class="page-heading"><div><div class="eyebrow">YOUR INVESTMENTS</div><h1>My portfolio</h1><p class="subtitle">Track position values and unrealized performance.</p></div><a class="btn btn-primary" href="{{ url_for('stock_market') }}">＋ Find investments</a></div>
      <div class="grid">
        <div class="card metric-card"><div class="metric-label">Total market value</div><div class="metric-value">{{ money(total_value) }}</div><div class="metric-foot">Value at current demo prices</div></div>
        <div class="card metric-card"><div class="metric-label">Total invested cost</div><div class="metric-value">{{ money(total_cost) }}</div><div class="metric-foot">Cost basis of open positions</div></div>
        <div class="card metric-card"><div class="metric-label">Unrealized P/L</div><div class="metric-value {{ 'positive' if profit_loss >= 0 else 'negative' }}">{{ money(profit_loss) }}</div><div class="metric-foot">Excludes realized gains and losses</div></div>
      </div>
      <section class="card">
        <div class="section-head"><div><h2>Open positions</h2><p class="subtitle" style="margin-top:5px">Sell shares from an existing position</p></div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Asset</th><th>Quantity</th><th>Average cost</th><th>Market price</th><th>Market value</th><th>Unrealized P/L</th><th>Sell</th></tr></thead>
          <tbody>{% for h in holdings %}
          <tr>
            <td><div class="stock-cell"><div class="stock-badge">{{ h.symbol[:2] }}</div><div><div class="stock-name">{{ h.name }}</div><div class="stock-symbol">{{ h.symbol }}</div></div></div></td>
            <td>{{ h.quantity }}</td><td>{{ money(h.average_price) }}</td><td>{{ money(h.market_price) }}</td><td style="font-weight:700">{{ money(h.value) }}</td>
            <td class="{{ 'positive' if h.profit_loss >= 0 else 'negative' }}">{{ money(h.profit_loss) }}</td>
            <td><form class="inline-form" method="POST" action="{{ url_for('sell_stock') }}"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}"><input type="hidden" name="symbol" value="{{ h.symbol }}"><input class="qty" type="number" name="quantity" min="1" max="{{ h.quantity }}" value="1" required><button class="btn btn-danger btn-small" type="submit">Sell</button></form></td>
          </tr>
          {% else %}<tr><td colspan="7" class="empty">Your portfolio is empty. Visit the market to buy your first demo shares.</td></tr>{% endfor %}</tbody>
        </table></div>
      </section>

      {% elif page == 'transactions' %}
      <div class="page-heading"><div><div class="eyebrow">ACCOUNT ACTIVITY</div><h1>Transactions</h1><p class="subtitle">A complete record of deposits and simulated stock orders.</p></div></div>
      <section class="card">
        <div class="section-head"><div><h2>Transaction ledger</h2><p class="subtitle" style="margin-top:5px">Most recent activity appears first</p></div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Transaction</th><th>Instrument</th><th>Quantity</th><th>Unit price</th><th>Total amount</th><th>Date & time</th></tr></thead>
          <tbody>{% for t in transactions %}
          <tr><td><span class="pill {{ 'down' if t.transaction_type == 'BUY' else '' }}">{{ t.transaction_type }}</span></td><td><strong>{{ t.symbol }}</strong></td><td>{{ t.quantity }}</td><td>{{ money(t.price) }}</td><td style="font-weight:700">{{ money(t.total) }}</td><td class="muted">{{ t.created_at }}</td></tr>
          {% else %}<tr><td colspan="6" class="empty">No transactions have been recorded yet.</td></tr>{% endfor %}</tbody>
        </table></div>
      </section>
      {% endif %}

      <div class="footer">Bubu Finance © {{ year }} · Educational simulation only · No real money or securities are involved</div>
    </div>
  </main>
</div>
{% endif %}
</body>
</html>
"""


# =====================================================
# START APPLICATION
# =====================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
