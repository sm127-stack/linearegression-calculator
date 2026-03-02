import os
import json
from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

USERS_FILE = "users.json"


# --------------------------
# Helper functions
# --------------------------

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


# --------------------------
# Routes
# --------------------------

@app.get("/")
def root():
    return redirect("/guest")


@app.get("/guest")
def guest():
    return redirect("/voila/render/guestversion.ipynb")


@app.get("/member")
def member():
    if not session.get("user"):
        return redirect("/guest")
    return redirect("/voila/render/memberversion.ipynb")


# --------------------------
# LOGIN
# --------------------------

@app.post("/login")
def login():
    email = request.form.get("email", "").lower()
    psw = request.form.get("psw", "")

    users = load_users()

    if email in users and users[email] == psw:
        session["user"] = email
        return redirect("/member")

    return redirect("/guest")


# --------------------------
# SIGN UP  ⭐ NEW
# --------------------------

@app.post("/signup")
def signup():
    email = request.form.get("email", "").lower()
    psw = request.form.get("psw", "")

    if not email or not psw:
        return redirect("/guest")

    users = load_users()

    # If user already exists → just log them in
    if email in users:
        session["user"] = email
        return redirect("/member")

    # Save new user
    users[email] = psw
    save_users(users)

    session["user"] = email
    return redirect("/member")
