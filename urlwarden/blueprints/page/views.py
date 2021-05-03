from flask import Blueprint, redirect, render_template, session

page = Blueprint("page", __name__, template_folder="templates")


@page.route("/", methods=["GET"])
def home():
    return render_template("page/home.html")


@page.route("/terms", methods=["GET"])
def terms():
    return render_template("page/terms.html")


@page.route("/privacy", methods=["GET"])
def privacy():
    return render_template("page/privacy.html")


@page.route("/myurls", methods=["GET"])
def myurls():
    if not session.get("user"):
        return redirect("/login")
    return render_template("page/myurls.html")


@page.route("/login", methods=["GET"])
def login():
    return render_template("page/login.html")
