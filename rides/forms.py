from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import widgets
from .models import User

# from .models import 

class UserSignUp(UserCreationForm):
    Choices = (
        ("1","Driver"),
    )
    driver = forms.ModelMultipleChoiceField(
        choices=Choices,
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta(UserCreationForm.Meta):
        model = User
