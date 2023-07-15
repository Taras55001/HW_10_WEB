from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegistrationForm(UserCreationForm):
    pass

class LoginForm(AuthenticationForm):
    pass
