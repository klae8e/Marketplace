from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path

from . import views
from .views import profile_view, RegisterView
from django.contrib import admin
from django.urls import path, include

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', profile_view, name='profile'),
    path('accounts/login/', LoginView.as_view(), name='login', kwargs={'redirect_authenticated_user': True}),
    path('accounts/logout/', LogoutView.as_view(next_page='main:profile'), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]