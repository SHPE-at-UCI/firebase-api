from flask import Flask, render_template, request, redirect, url_for, make_response
from apscheduler.schedulers.background import BackgroundScheduler
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import atexit
import sqlite3
import sheets_api
import requests

app = Flask(__name__)
scheduler = None
data_buffer = sheets_api.buffer()
running_flush = False
waiting_flush = False

#empty a non-empty buffer to sheet
def flush_buffer():
    global data_buffer, running_flush, waiting_flush    
    completed = True
    if(len(data_buffer)!=0):
        print("Flushing buffer")
        data = data_buffer.process()
        try:
            running_flush = True
            sendData(data)
        except Exception as e:
            print("Error occured in flush:\n\t", e)
            #for item in data:
            #    data_buffer.add(item)
            data_buffer = sheets_api.buffer(data)
            completed = False
        finally:
            running_flush = False
    #check if there is also a waiting_flush, if so complete it
    while(waiting_flush and len(data_buffer)!=0):
        print("Flushing buffer")
        data = data_buffer.process()
        try:
            running_flush = True
            sendData(data)
        except Exception as e:
            print("Error occured in coalesced flush:\n\t", e)
            #for item in data:
            #    data_buffer.add(item)
            data_buffer = sheets_api.buffer(data)
            completed = False
        finally:
            waiting_flush = False
            running_flush = False
    return completed
    
#make sure we have access to sheets and then write it to sheet
def sendData(data):
    sheets_api.sign_in()
    sheets_api.addMultiple(data)
    
#make sure that all cancelled, the buffer has been successfully saved
def shutdown():
    print("\nShutting down server...")
    for job in scheduler.get_jobs():
        job.remove()
        
    #save data buffer for reuse upon restart
    global data_buffer
    with open(".buffer", 'w') as buf:
        buf.write(repr(data_buffer))
    #if(not flush_buffer()):
    #    print("Flush failed!\n\tcurrent state of data_buffer:", data_buffer)
    
        
    print("Killing scheduler")
    scheduler.shutdown()
    print("Shutdown.")
        
@app.before_first_request
def init_scheduler():
    print("Server starting up...")
    sheets_api.sign_in()
    
    global data_buffer
    with open(".buffer", 'r') as buf:
        data = eval(buf.read())
        if data:
            print("Loading data buffer")
            data_buffer = data

    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()
    
    #add a job to infrequently flush the buffer if there is data but not
    #enough to fill the buffer
    import os
    scheduler.add_job(name='Timed flush', id="job_1", func=flush_buffer, trigger='interval', hours=int(os.getenv("FLUSH_HOURS")), minutes=int(os.getenv("FLUSH_MINUTES")))
    del os
    
    # Schedule shutdown to occur when exiting the app
    atexit.register(lambda: shutdown())
    
    print("Server started")


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        email = request.form["emailInput"]   
         
        global data_buffer
        data_buffer.add(email)
        print("Data Buffer:", data_buffer)
        
        
        #if our buffer has enough data in it, we'll just flush it to sheets
        if(data_buffer.is_filled()):
            #we flush it as background job to make sure it doesnt slow anyones responses
            global scheduler, running_flush, waiting_flush
            #if theres currently a flush already occuring, note impending flush, otherwise schedule
            if(running_flush):
                waiting_flush = True
            else:
                scheduler.add_job(name='Filled flush', id="job_2", func=flush_buffer, trigger='date')        	 
        	      
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

@app.route("/register", methods=('GET','POST'))
def register_page():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        major = request.form['major']
        year = request.form['year']
        username = firstName + lastName
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
        return redirect(webauth)q
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
