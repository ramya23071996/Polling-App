from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from . import db, r
from .models import Poll, User

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    polls = Poll.query.all()
    return render_template("index.html", polls=polls)

@main.route("/vote/<int:poll_id>", methods=["POST"])
def vote(poll_id):
    choice = request.form["choice"]
    r.hincrby(f"poll:{poll_id}", choice, 1)
    return "", 204

@main.route("/admin", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        question = request.form["question"]
        choices = request.form.getlist("choices")
        db.session.add(Poll(question=question, choices=choices))
        db.session.commit()
    polls = Poll.query.all()
    return render_template("dashboard.html", polls=polls)