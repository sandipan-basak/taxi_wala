import random
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
# from django.forms import widgets
from .models import User, Executive, Rider, Ride, Place
# from phonenumber_field.formfields import PhoneNumberField
# from crispy_forms.helper import FormHelper

class RiderSignUpForm(UserCreationForm):
    # cell = PhoneNumberField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'username', 'password1', 'password2', 'cell')

    def __init__(self, *args, **kwargs):
        super(RiderSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['name','username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_rider = True
        user.save()
        Rider.objects.create(user=user)
        return user

class ExecutiveSignUpForm(UserCreationForm):
   
    shift_options = (('M','08:00 - 17:00'),('E','16:00 - 01:00'),('N','00;00 - 09:00'))
    shift = forms.ChoiceField(choices=shift_options)
    car = forms.CharField(min_length=5)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'password1', 'password2', 'shift', 'cell', 'car')
       
    def __init__(self, *args, **kwargs):
        super(ExecutiveSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['name', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def generate_digits(self, amount):
        digits = ""
        for _ in range(amount):
            digits = digits + chr(random.randint(ord('0'), ord('0')+9))
        return digits

    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        user = super().save(commit=False)        
        user.username = "_".join(user.name.split().append(self.generate_digits(7)))
        user.is_executive = True
        ex = Executive.objects.create(user=user)
        ex.shift = data.get('shift')
        
        # ex.car = data.get('car')
        return user

class BookRideViewForm(forms.ModelForm):
    
    source = forms.CharField(max_length=250)
    destination = forms.CharField(max_length=250)
    class Meta:
        model = Place
        fields = ('source','destination',)

    

    