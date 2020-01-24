from flask import Flask , render_template
import sqlite3
app = Flask(__name__, static_folder="../static/dist",
            template_folder="../static")

@app.route("/")
def index():
    return "hello"

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

if __name__ == "__main__":
    app.run()
