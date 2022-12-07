from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    username = models.TextField(blank=True, null=True)
    email = models.EmailField("email address", unique=True)
    timezone_Shift = models.IntegerField()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return "{}".format(self.email)
