from django.urls import path

from . import views
from .views import profile_view

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", profile_view, name="profile"),
]