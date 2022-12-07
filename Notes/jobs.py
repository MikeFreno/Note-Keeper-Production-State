from schedule import Scheduler
import schedule
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from .models import Reminder
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
import os
import random
import threading
import time


def find_today_and_tomorrow_remiders():
    print("listing started")
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
            hour = time_[0]
            if reminder.time.split(" ")[1] == "PM":
                hour = str(int(hour) + 12)
            min = time_[1].split(" ")[0]
            timezone = reminder.author.timezone_Shift
            timezone_minutes = (timezone % 1) * 60
            hour = int(hour) + int(timezone)
            min = int(min) + timezone_minutes
            day = int(date[1])
            month = int(date[0])
            year = int(date[2])
            if min >= 60:
                min -= 60
                hour += 1
            if hour >= 24:
                hour -= 24
                day += 1
            if day == 32:
                day = 1
                month += 1
            elif month == 4 or month == 6 or month == 9 or month == 11:
                if day == 31:
                    day = 1
                    month += 1
            elif month == 2 and day >= 29:
                day = 1
                month += 1
            if month == 13:
                month = 1
                year += 1
            date_time = datetime(year=year, month=month, day=day, hour=hour, minute=min)
            list_to_queue.append(
                {
                    "reminder": reminder,
                    "description": reminder.description,
                    "user": reminder.author.email,
                    "time": date_time,
                },
            )
    print("pass make list")
    emailer_offload_to_sendgrid(list_to_queue)


def emailer_offload_to_sendgrid(list_to_queue):
    print("handoff")
    configuration = sib_api_v3_sdk.Configuration()
    load_dotenv(find_dotenv())
    KEY = os.environ["SENDINBLUE_KEY"]
    for reminder in list_to_queue:
        print(reminder)
        email = reminder["user"]
        desc = reminder["description"]
        configuration.api_key["api-key"] = KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        subject = "Here is Your Reminder"
        sender = {"name": "Michael Freno", "email": "mike@notesapp.net"}
        templateId = 3
        to = [{"email": email}]
        scheduledAt = reminder["time"]
        params = {"LASTNAME": desc}
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            template_id=templateId,
            sender=sender,
            subject=subject,
            scheduled_at=scheduledAt,
            params=params,
        )
        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
        except ApiException as e:
            print("Exception when calling S`MTPApi->send_transac_email: %s\n" % e)
            to_set = reminder["reminder"]
            to_set.queued = False


def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously  # type: ignore


def start_scheduler():
    scheduler = Scheduler()
    scheduler.every(12).hours.do(find_today_and_tomorrow_remiders)
    scheduler.run_continuously()  # type: ignore
