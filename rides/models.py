from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, mark_safe

# Create your models here.
class User(AbstractUser):
    is_rider = models.BooleanField(default=False)
    is_ex = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    cell = models.IntegerField(blank=True, unique=True)

class Location(models.Model):
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    address = models.CharField(max_length=200)


class Executive(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    shift = models.IntegerField(default=1)
    avg_r = models.DecimalField(max_digits=2, decimal_places=1)
    amount = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return self.user.username

class Cabs(models.Model):
    number = models.CharField(max_length=20)
    executive = models.OneToOneField(Executive, on_delete=models.CASCADE, primary_key=True)
    lat = models.DecimalField(max_digits=20, decimal_places=14)
    lon = models.DecimalField(max_digits=20, decimal_places=14)

class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.user.username

class Status(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.name)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

# class RideAlert(models.Model):
#     rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
#     
    

class Rides(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    cabee = models.ForeignKey(Executive, on_delete=models.CASCADE)
    cab = models.ForeignKey(Cabs, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    
    def __str__(self):
        return self.pk
