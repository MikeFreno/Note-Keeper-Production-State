from rest_framework import serializers
from .models import Task, Reminder


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "completed", "author")


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ("id", "title", "description", "date", "time", "completed", "author")
