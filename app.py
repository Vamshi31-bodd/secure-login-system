import os
import re
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import IntegrityError

from database import db, User

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY missing from .env")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = (
    os.getenv("COOKIE_SECURE", "false").lower() == "true"
)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

db.init_app(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://"
)

with app.app_context():
    db.create_all()


def validate_password(password):
    if len(password) < 10:
        return "Password must be at least 10 characters."

    if not re.search(r"[A-Z]", password):
        return "Add at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return "Add at least one lowercase letter."

    if not re.search(r"\d", password):
        return "Add at least one number."

    if not re.search(r"[^A-Za-z0-9]", password):
        return "Add at least one special character."

    return None


@app.route("/")
def home():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def register():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        if len(username) < 3 or len(username) > 50:
            flash("Username must be 3 to 50 characters.", "danger")
            return render_template("register.html")

        if not re.fullmatch(r"[\w.@+-]+@[\w.-]+\.[A-Za-z]{2,}", email):
            flash("Enter a valid email address.", "danger")
            return render_template("register.html")

        error = validate_password(password)
        if error:
            flash(error, "danger")
            return render_template("register.html")

        existing = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()

        if existing:
            flash("An account with this email already exists.", "danger")
            return render_template("register.html")

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Registration could not be completed. Try again.", "danger")
            return render_template("register.html")

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Enter your email and password.", "danger")
            return render_template("login.html")

        user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()

        if user is None or not bcrypt.check_password_hash(
            user.password_hash, password
        ):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        session.clear()
        session.permanent = True
        session["user_id"] = user.id

        flash("Login successful!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")

    if not user_id:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    user = db.session.get(User, user_id)

    if user is None:
        session.clear()
        flash("Session expired. Please log in again.", "warning")
        return redirect(url_for("login"))

    return render_template("dashboard.html", user=user)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.errorhandler(429)
def rate_limit_error(error):
    flash("Too many attempts. Please wait a minute before trying again.", "warning")
    return render_template("login.html"), 429


if __name__ == "__main__":
    app.run()