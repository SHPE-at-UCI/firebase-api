from flask import Flask, render_template, request, redirect, make_response, url_for
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import sqlite3
import requests
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
    
def refresh_login_status():
    login_status = {}
    uci_cookie = "ucinetid_auth"
    
    if(uci_cookie in request.cookies):
        param = urlencode({uci_cookie: request.cookies.get(uci_cookie)})
        webauth_check = 'http://login.uci.edu/ucinetid/webauth_check'
        resp = requests.get(webauth_check+"?"+param).content.decode("utf-8")
        
        for line in resp.split("\n"):
            key_val = line.split("=")
            if(len(key_val)!=2 or key_val[1]==''):
                continue
            elif(len(key_val)==2 and key_val[0]=="uci_affiliations"):
                login_status[key_val[0]] = set(key_val[1].split(","))
            else:
                login_status[key_val[0]] = key_val[1]
                
        login_status['valid'] = False
        if('error_code' in login_status or 'auth_fail' in login_status):
            print("Error Code:",login_status.get('error_codes'))
            print("Authentication Failure:",login_status.get('auth_fail'))
        elif('ucinetid' in login_status and 'time_created' in login_status and login_status['auth_host'] == login_status['x_forwarded_for']):
            login_status['valid'] = True
        
    return login_status    
             

@app.route("/login")
def login():
    resp = None
    param = urlencode({"return_url": "http://shpe.uci.edu:5000"})
    webauth = 'http://login.uci.edu/ucinetid/webauth?' + param
    
    login_status = refresh_login_status()
    if(login_status['valid']):
        return "Already logged in as "+login_status['ucinetid']#redirect("/")
        #resp = make_response(redirect("/"))
        #resp.set_cookie('SHPE', 'logged in')
    else:
        return redirect(webauth)
        #resp = make_response(redirect(webauth))
        #resp.set_cookie('SHPE', 'login')
    #return resp
    
@app.route("/logout")
def logout():
    resp = None
    param = urlencode({"return_url": "http://shpe.uci.edu:5000"})
    webauth = 'http://login.uci.edu/ucinetid/webauth_logout?' + param
    
    login_status = refresh_login_status()
    if(login_status['valid']):
        return redirect(webauth)
        #resp = make_response(redirect(webauth))
        #resp.set_cookie('SHPE', 'logout')
    else:
        return "Not logged in"#redirect("/")
        #resp = make_response(redirect("/"))
        #resp.set_cookie('SHPE', 'logged out')
    #return resp
    
    

if __name__ == "__main__":
    app.run()
