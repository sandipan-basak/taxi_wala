from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import widgets
from rides.models import User, Executive, Rider, Rides

from crispy_forms.helper import FormHelper

class RiderSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'username')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_rider = True
        user.save()
        Rider.objects.create(user=user)
        return user

class ExecutiveSignUpForm(UserCreationForm):
    
    shift_options = (('1','8-17'),('2','16-1'),('0','0-9'))
    shift = forms.ChoiceField(choices=shift_options)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'password1', 'password2', 'shift', 'cell')
       
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_executive = True
        user.username = user.name
        ex = Executive.objects.create(user=user)
        ex.shift
        return user

class BookRideViewForm(forms.ModelForm):    
    class Meta:
        model = Rides
        fields = ('source','destination',)
    