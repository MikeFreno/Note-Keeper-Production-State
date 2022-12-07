from django.apps import AppConfig
import os


class NotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Notes"

    def ready(self):
        from . import jobs

        if os.environ.get("RUN_MAIN", None) != "true":
            print("started")
            jobs.start_scheduler()
