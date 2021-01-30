from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import widgets
from .models import User, Executive, Rider

class RiderSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ('name', 'user_name', 'password', 'cell')
        model = Rider

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_rider = True
        if commit:
            user.save()
        return user

class ExecSignUpForm(UserCreationForm):
  
    class Meta(UserCreationForm.Meta):
        fields = ('name', 'shift', 'cell')
        model = Executive
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_ex = True
        if commit:
            user.save()
        return user