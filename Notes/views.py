from django.shortcuts import render
from rest_framework import viewsets

from .serializers import TaskSerializer, ReminderSerializer
from .models import Task, Reminder


# Create your views here.
def index(request):
    return render(request, "index.html")


class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(author=self.request.user.pk)


class ReminderView(viewsets.ModelViewSet):
    serializer_class = ReminderSerializer
    queryset = Reminder.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(author=self.request.user.pk)
