from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, mark_safe
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    is_rider = models.BooleanField(default=False)
    is_ex = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    cell = PhoneNumberField(blank=True)
    wallet = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    def __str__(self):
        return self.username

# class Place(models.Model):
#     pincode = models.CharField(max_length=10)
#     state = models.CharField(max_length=120)
#     city = models.CharField(max_length=120)
#     country = models.CharField(max_length=120)
#     address = models.CharField(max_length=200)

class Cab(models.Model):
    number = models.CharField(max_length=20, unique=True)
    lat = models.DecimalField(max_digits=20, decimal_places=14)
    lng = models.DecimalField(max_digits=20, decimal_places=14)
    curr_save_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    class Meta():
        ordering = ['number']
    
    def __str__(self):
        return self.number

class Executive(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    car = models.OneToOneField(Cab, on_delete=models.CASCADE, null=True, blank=False)
    shift = models.CharField(max_length=1)
    avg_r = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    def __str__(self):
        return self.user.username

class Status(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Status"

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.name)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class Ride(models.Model):
    rider = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cabee = models.ForeignKey(Executive, on_delete=models.CASCADE, null=True, blank=True)
    cab = models.ForeignKey(Cab, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    travelled = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    charges = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    source = models.CharField(max_length=200, blank=False)
    destination = models.CharField(max_length=200, blank=False)
    
    def __str__(self):
        return str(self.pk)
