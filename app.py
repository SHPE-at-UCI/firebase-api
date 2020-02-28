from flask import Flask, render_template, request
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


@app.route("/delete")
def delete():
    return "Delete"


if __name__ == "__main__":
    app.run()
