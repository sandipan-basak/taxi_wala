from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_rider = models.BooleanField(default=False)
    is_ex = models.BooleanField(default=False)


class Executive(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # name = models.CharField(max_length=120)
    shift = models.BooleanField(default=True)
    cell = models.IntegerField(null=False, blank=False, unique=True)
    cab = models.OneToOneField(Cabs,)
    avg_r = models.DecimalField(max_digits=1, decimal_places=1)

class Cabs(models.Model):
    number = models.CharField(max_length=20)
    ex = models.OneToOneField(Executive, on_delete=models.CASCADE, primary_key=True)
class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # name = models.CharField(max_length=120)
    cell = models.IntegerField(max_length=12, null=False, blank=False, unique=True)

    def __str__(self):
    return self.user.username
    # user_name = models.CharField(max_length=100)

class Rides(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    ex = models.ForeignKey(Executive, on_delete=models.CASCADE)
    cab = models.ForeignKey(Cabs, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    rating = models.IntegerField(max_length=1, default=0)