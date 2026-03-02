import os
import json
from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

USERS_FILE = "users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except Exception:
        # If file is corrupted, just reset users
        return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f)


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


@app.post("/login")
def login():
    email = request.form.get("email", "").strip().lower()
    psw = request.form.get("psw", "")

    users = load_users()
    if email in users and users[email] == psw:
        session["user"] = email
        return redirect("/member")

    return redirect("/guest")


@app.post("/signup")
def signup():
    email = request.form.get("email", "").strip().lower()
    psw = request.form.get("psw", "")

    if not email or not psw:
        return redirect("/guest")

    users = load_users()
    if email not in users:
        users[email] = psw
        save_users(users)

    session["user"] = email
    return redirect("/member")

@app.get("/ping")
def ping():
    return "pong"
