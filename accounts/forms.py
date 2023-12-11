from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django import forms

from accounts.models import User


class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["email", "username"]

class AuthForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "autofocus": True}),
    )