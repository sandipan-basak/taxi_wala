import random
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import widgets
from .models import User, Executive,  Ride, Place
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

class RiderSignUpForm(UserCreationForm):

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
        user.set_password(self.cleaned_data["password1"])
        user.is_rider = True
        user.save()
        # Rider.objects.create(user=user)
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
        user.set_password(data.get('password1'))
        user.username = "_".join(user.name.split().append(self.generate_digits(7)))
        user.is_ex = True
        
        ex = Executive.objects.create(user=user)
        ex.shift = data.get('shift')
        return user

class BookRideViewForm(forms.ModelForm):
    
    class Meta:
        model = Ride
        fields = ('source', 'destination')

        widgets = {
            'source': forms.HiddenInput,
            'destination': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(BookRideViewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('source', css_id="pickup_loc", css_class="search_p w-100 col-11", type="text", placeholder="Pickup..."),
            Field('destination', css_class="search_d w-100 col-11", css_id="drop_loc", type="text", placeholder="Drop..."),
        )
    
    # def save(self):
    #     data = self.cleaned_data
    #     ride = super().save(commit=False)
    #     ride.


    

