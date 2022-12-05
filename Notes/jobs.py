import schedule
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, From, Subject, Content, SendAt
from .models import Reminder
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
import os
import random
import time


def find_today_and_tomorrow_remiders():
    now = datetime.now()
    today = str(now.strftime(f"%m/%d/%Y"))
    time_delta = datetime.now() + timedelta(1)
    tomorrow = str(time_delta.strftime(f"%m/%d/%Y"))
    reminders = Reminder.objects.all()
    list_to_queue = []
    for reminder in reminders:
        if (
            reminder.completed == False
            and reminder.queued == False
            and (reminder.date == today or reminder.date == tomorrow)
        ):
            date = reminder.date.split("/")
            time_ = reminder.time.split(":")
            hour = int(time_[0]) - reminder.author.timezone_Shift
            min = time_[1].split(" ")[0]
            date_time = datetime(
                year=int(date[2]),
                month=int(date[0]),
                day=int(date[1]),
                hour=int(hour),
                minute=int(min),
            )
            unix_time = int(time.mktime(date_time.timetuple()))

            list_to_queue.append(
                [
                    {
                        "reminder": reminder,
                        "description": reminder.description,
                        "user": reminder.author.email,
                        "time": unix_time,
                    },
                ]
            )
    emailer_offload_to_sendgrid(list_to_queue)


css_styles = """<style>
      html {
        margin: 2em 1em 1em 2em;
        font-size: larger;
      }
      .body {
        margin: 2em 1em 1em 2em;
        font-family: "Poppins", sans-serif;
        background-color: #3f4e4f;
        width: 100vw;
        color: #a27b5c;
      }
      h2 {
        background-color: #3f4e4f;
      }
      .text-center {
        background-color: #3f4e4f;
      }
    </style>"""
goodbye_list = ["-KBYE", "-See ya", "-Thanks for using the app!", "-Have a good one :)"]


def emailer_offload_to_sendgrid(list_to_queue):
    load_dotenv(find_dotenv())
    SECRET_KEY = os.environ["SENDGRID_API_KEY"]
    bye = random.choice(goodbye_list)
    for reminder in list_to_queue:
        print("pass")
        desc = reminder["description"]
        message = Mail()
        message.to = [
            To(
                email=reminder["email"],
            ),
        ]
        message.from_email = From(
            email="michael@freno.me",
            name="Michael Freno",
        )
        message.content = [
            Content(
                mime_type="text/html",
                content=f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    {css_styles}
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
    />
  </head>
  <body class="body">
    <h2 class="text-center">Hey!</h2>
    <div class="text-center">This is your reminder for {desc}</div>
    <div class="text-center">{bye}</div>
    <br /><br /><br />
    <div class="text-center" style="font-size: medium">
      You can adjust these emails in the user settings at<br /><a
        style="color: #a27b5c"
        href="https://notesapp.net"
        >notesapp.net</a
      >
    </div>
  </body>
</html>
""",
            )
        ]
        message.send_at = SendAt(reminder["time"])
        message.subject = Subject(reminder["description"])
        sendgrid_client = SendGridAPIClient(SECRET_KEY)

        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        to_set = reminder["reminder"]
        to_set.queued = False


schedule.every(12).hours.do(find_today_and_tomorrow_remiders)


def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
