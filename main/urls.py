from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .views import profile_view
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", profile_view, name="profile"),
    path('accounts/login/', LoginView.as_view(), name='login', kwargs={'redirect_authenticated_user': True}),
    path('accounts/logout/', LogoutView.as_view(next_page='profile'), name='logout'),
]