from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.shortcuts import reverse



class LoginView(LoginView):
    
    def get_success_url(self):
        return reverse('home')

class LogoutView(LogoutView):
    next_page = ('home')

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('users:login')