from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import os
import sheets_api


class SheetsApiClient:

    scheduler = None
    data_buffer = sheets_api.buffer()
    running_flush = False
    waiting_flush = False

    def __init__(self):
        print("Server starting up...")
        sheets_api.sign_in()

        global data_buffer
        with open(".buffer", "r") as buf:
            data = eval(buf.read())
            if data:
                print("Loading data buffer")
                data_buffer = data

        global scheduler
        scheduler = BackgroundScheduler()
        scheduler.start()

        # add a job to infrequently flush the buffer if there is data but not
        # enough to fill the buffer

        scheduler.add_job(
            name="Timed flush",
            id="job_1",
            func=self.flush_buffer,
            trigger="interval",
            hours=int(os.getenv("FLUSH_HOURS")),
            minutes=int(os.getenv("FLUSH_MINUTES")),
        )

        # Schedule shutdown to occur when exiting the app
        atexit.register(lambda: self.shutdown())

        print("Server started")

    # make sure we have access to sheets and then write it to sheet
    def sendData(self, data):
        sheets_api.sign_in()
        sheets_api.addMultiple(data)

    # make sure that all cancelled, the buffer has been successfully saved
    def shutdown(self):
        print("\nShutting down server...")
        for job in scheduler.get_jobs():
            job.remove()

        # save data buffer for reuse upon restart
        global data_buffer
        with open(".buffer", "w") as buf:
            buf.write(repr(data_buffer))

        print("Killing scheduler")
        scheduler.shutdown()
        print("Shutdown.")

    def signin_user(self, user):
        global data_buffer
        data_buffer.add(user)
        print("Data Buffer:", data_buffer)

        # if our buffer has enough data in it, we'll just flush it to sheets
        if data_buffer.is_filled():
            # we flush it as background job to
            # make sure it doesnt slow anyones responses
            global scheduler, running_flush, waiting_flush

            # if theres currently a flush already occuring
            # note impending flush otherwise schedule
            if running_flush:
                waiting_flush = True
            else:
                scheduler.add_job(
                    name="Filled flush",
                    id="job_2",
                    func=self.flush_buffer,
                    trigger="date",
                )

        return "thank you"

    # empty a non-empty buffer to sheet
    def flush_buffer(self):
        global data_buffer, running_flush, waiting_flush
        completed = True
        if len(data_buffer) != 0:
            print("Flushing buffer")
            data = data_buffer.process()
            try:
                running_flush = True
                self.sendData(data)
            except Exception as e:
                print("Error occured in flush:\n\t", e)
                for item in data:
                    data_buffer.add(item)
                # data_buffer = sheets_api.buffer(data)
                completed = False
            finally:
                running_flush = False
        # check if there is also a waiting_flush, if so complete it
        while waiting_flush and len(data_buffer) != 0:
            print("Flushing buffer")
            data = data_buffer.process()
            try:
                running_flush = True
                self.sendData(data)
            except Exception as e:
                print("Error occured in coalesced flush:\n\t", e)
                for item in data:
                    data_buffer.add(item)
                # data_buffer = sheets_api.buffer(data)
                completed = False
            finally:
                waiting_flush = False
                running_flush = False
        return completed
