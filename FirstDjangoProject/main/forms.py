# from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import *
from users.models import User
# from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class LogInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


# class CustomPasswordResetForm(PasswordResetForm):
#     def clean_email(self):
#         email = self.cleaned_date.get('email', '')
#         if not User.objects.filter(email=email):
#             raise forms.ValidationError('Почтовый ящик не зарегистрирован')
#         return email
