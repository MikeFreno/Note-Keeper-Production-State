"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from Notes import views
from authAPI import views as v


router = routers.DefaultRouter()
router.register(r"tasks", views.TaskView, "task")
router.register(r"reminders", views.ReminderView, "reminder")
router.register(r"users", v.UserView, "user")
# router.register(r"user_timezones", v.TimezoneUpdateView, "user_timezones")

urlpatterns = [
    path("", views.index, name="index"),
    path("api/auth/login/state/", v.user_state),
    path("api/emailer/register/", v.registration_emailer),
    # path("api/users/timezones", v.patch),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
]
