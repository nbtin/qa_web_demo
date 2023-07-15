from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import sys
from django import forms

sys.path.append("..")


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']