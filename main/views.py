from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from main.forms import RegisterForm


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

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('main:profile')
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

