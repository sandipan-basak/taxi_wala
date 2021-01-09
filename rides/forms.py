from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import widgets
from .models import User

# from .models import 

class UserSignUp(UserCreationForm):

    
    class Meta(UserCreationForm.Meta):
        fields = ('username','name','password')
        model = User
    

