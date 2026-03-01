import os
from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

MEMBER_EMAIL = os.environ.get("MEMBER_EMAIL", "member@example.com")
MEMBER_PASS  = os.environ.get("MEMBER_PASS",  "changeme")


@app.get("/")
def root():
    return redirect("/guest")


@app.get("/guest")
def guest():
    return redirect("/voila/render/guestversion.ipynb")


@app.get("/member")
def member():
    if not session.get("logged_in"):
        return redirect("/guest")
    return redirect("/voila/render/memberversion.ipynb")


@app.post("/login")
def login():
    email = request.form.get("email", "")
    psw = request.form.get("psw", "")

    if email == MEMBER_EMAIL and psw == MEMBER_PASS:
        session["logged_in"] = True
        return redirect("/member")

    return redirect("/guest")
