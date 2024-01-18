from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


@login_required
def profile_view(request):
    return render(request, 'main/profile.html')

def sign_in(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("main/profile.html")

    else:
        # Return an 'invalid login' error message.
        print('error')

