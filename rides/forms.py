from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import widgets
from .models import User, Executive, Rider, Rides

from crispy_forms.helper import FormHelper

class RiderSignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RiderSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
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
    
    shift_options = (('Shift 1','08:00 - 17:00'),('Shift 2','16:00 - 01:00'),('Shift 0','00;00 - 09:00'))
    shift = forms.ChoiceField(choices=shift_options)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'password1', 'password2', 'shift', 'cell')
       
    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        user = super().save(commit=False)
        user.is_executive = True
        ex = Executive.objects.create(user=user)
        ex.shift = data.get('shift')
        return user

class BookRideViewForm(forms.ModelForm):
    class Meta:
        model = Rides
        fields = ('source','destination',)
    