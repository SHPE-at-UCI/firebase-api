from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import sqlite3
import sheets_api

app = Flask(__name__)
scheduler = None
data_buffer = sheets_api.buffer()

#empty a non-empty buffer to sheet
def flush_buffer():
    global data_buffer
    if(len(data_buffer)!=0):
        print("Flushing buffer")
        data = data_buffer.process()
        try:
            sendData(data)
        except Exception as e:
            print("Error occured:\n\t", e)
            for item in data:
                data_buffer.add(item)
            return False
    return True
    
#make sure we have access to sheets and then write it to sheet
def sendData(data):
    sheets_api.sign_in()
    sheets_api.addMultiple(data)
    
#make sure that all cancelled, the buffer has been successfully
def shutdown():
    print("\nShutting down server...")
    for job in scheduler.get_jobs():
        job.remove()
    print("Flushing buffer")
    if(not flush_buffer()):
        print("Flush failed!\n\tcurrent state of data_buffer:", data_buffer)
    print("Killing scheduler")
    scheduler.shutdown()
    print("Shutdown.")
        
@app.before_first_request
def init_scheduler():
    print("Server starting up...")
    sheets_api.sign_in()

    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()
    
    #add a job to infrequently flush the buffer if there is data but not
    #enough to fill the buffer
    scheduler.add_job(name='Timed flush', id="job_1", func=flush_buffer, trigger='interval', hours=1)
    
    # Schedule shutdown to occur when exiting the app
    atexit.register(lambda: shutdown())
    print("Server started")


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        email = request.form["emailInput"]   
         
        global data_buffer
        data_buffer.add(email)
        print("data buffer:", data_buffer)
        
        
        #if our buffer has enough data in it, we'll just flush it to sheets
        if(data_buffer.is_filled()):
            #we flush it as a job to make sure it doesnt slow anyones responses
            global scheduler
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


@app.route("/delete")
def delete():
    return "Delete"



if __name__ == "__main__":
    app.run()
