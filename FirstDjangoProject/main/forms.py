# from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import *
from users.models import User
from profiles.models import Profile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class LogInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
