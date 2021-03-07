from django.contrib import admin
from .models import Executive, Cab, Rider, Ride, Status, Place, User
# Register your models here.

admin.site.register(Executive)
admin.site.register(Cab)
admin.site.register(Ride)
admin.site.register(Rider)
admin.site.register(Status)
admin.site.register(Place)
admin.site.register(User)
