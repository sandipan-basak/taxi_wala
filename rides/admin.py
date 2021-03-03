from django.contrib import admin
from .models import Executive, Cab, Rider, Rides, Status, Location, User
# Register your models here.

admin.site.register(Executive)
admin.site.register(Cab)
admin.site.register(Rides)
admin.site.register(Rider)
admin.site.register(Status)
admin.site.register(Location)
admin.site.register(User)
