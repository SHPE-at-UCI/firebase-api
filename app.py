from flask import Flask, render_template, request
import sqlite3
import sheets_api
app = Flask(__name__)


@app.route("/", methods=('GET', 'POST'))
def index():    
    if request.method == 'POST':
        email = request.form["emailInput"]   
         
         
        sheets_api.sign_in()
        #Find and AddNew take 2 API calls each
        #Option 1: Search for email, if exists say already signed in otherwise add the email
        if sheets_api.find(email) != -1:
        	print("This email already exists")
        else:
        	sheets_api.addNew(email)
        #Option 2: Add email to sheet, spreadsheet has separate list of unique email
        #####sheets_api.addNew(email)    
        #Option 3: Read email list into python and check if unique
        #####...        	
        	 
        	      
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
