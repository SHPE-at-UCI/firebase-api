from flask import Flask, render_template, request, redirect
import requests


app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        # TODO: create sheets-user-api.py
        
        # return signin_user(request.form["emailInput"])
        return redirect("/thank-you")
    
    return render_template("home.html")


@app.route("/create")
def create():
    return "Create"


@app.route("/read")
def read():
    return "Read"


@app.route("/update")
def update():
    return "Update"


@app.route("/delete")
def delete():
    return "Delete"


@app.route("/thank-you")
def success_page():
    return render_template("thank-you.html")


@app.route("/register", methods=("GET", "POST"))
def register_page():
    if request.method == "POST":
        # TODO: Understand why we were extracting these variables
        # firstName = request.form["firstName"]
        # lastName = request.form["lastName"]
        # email = request.form["email"]
        # major = request.form["major"]
        # year = request.form["year"]
        # username = firstName + lastName
        return redirect("/thank-you")  # render_template("thank-you.html")
    return render_template("register.html")


@app.route("/login")
def uci_signin():
    return "UCI login failed"


@app.route("/logout")
def logout():
    # TODO: Fix Login status so users can sign-in with UCI account
    return "UCI logout failed"


@app.errorhandler(404)
def page_not_found(err):
    # note that we set the 404 status explicitly
    return str(err), 404


if __name__ == "__main__":
    app.run()
