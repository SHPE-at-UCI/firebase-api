from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)


@app.route("/", methods=('GET', 'POST'))
def index():    
    if request.method == 'POST':
        email = request.form["emailInput"]                
        return render_template('thank-you.html')
    return render_template('home.html')


@app.route("/create")
def create():
    return "Create"


@app.route("/read")
def read():
    return "Read"


@app.route("/update")
def update():
    return "Update"

@app.route("/thank-you")
def success_page():
    return render_template("thank-you.html")
# This is for registerAlt.html, which is my slow progression on using Bootstrap to make the Register Page mobile friendly #
@app.route("/registerV2", methods=('GET','POST'))
def improved_register():
    return render_template("registerAlt.html")
###########################################################################################################################
@app.route("/register", methods=('GET','POST'))
def register_page():
    print("Can You See This")
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        major = request.form['major']
        year = request.form['year']
        username = firstName + lastName
        print(username)
        return render_template("thank-you.html")
    return render_template("register.html")

@app.route("/delete")
def delete():
    return "Delete"


if __name__ == "__main__":
    app.run()
