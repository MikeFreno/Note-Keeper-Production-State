from django.db import models
from authAPI.models import User


class Task(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return self.title


class Reminder(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    date = models.TextField(default="12/31/2050")
    time = models.TextField(default="12:00:00")
    queued = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return self.title
