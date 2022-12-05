from django.contrib import admin
from .models import Task, Reminder


class TasksAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "completed")


class RemindersAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "date", "time", "completed")


# Register your models here.

admin.site.register(Task, TasksAdmin)
admin.site.register(Reminder, RemindersAdmin)
