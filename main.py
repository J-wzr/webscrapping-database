import smtplib
import ssl
import time
import requests
import selectorlib
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event:

    def scrape(self, url):
        request = requests.get(url, headers=HEADERS)
        source = request.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:

    def send(message):
        host = "smtp.gmail.com"
        port = 465
        SENDER = "your email"
        PASSWORD = "your password"
        RECEIVER = "receiver email"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, RECEIVER, message)

        print("Email Sent")


class Database:

    def __init__(self, database_path) -> None:
        self.connection = sqlite3.connect(database_path)

    def store(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()

    def read(self, extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        return rows



if __name__ == "__main__":
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)
        
        
        if extracted != "No upcoming tours":
            database = Database(database_path="data.db")
            row = database.read(extracted)
            if not row:
                database.store(extracted)
                email = Email()
                email.send(message="Hey, A new event was found!")
            time.sleep(1)