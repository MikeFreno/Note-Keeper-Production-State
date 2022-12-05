from django.apps import AppConfig
import os


class NotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Notes"

    def runner():
        from . import jobs

        print("pass")
        jobs.scheduler()
