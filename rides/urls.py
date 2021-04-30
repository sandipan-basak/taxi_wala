from django.urls import path, include
from .views import rides, executive, rider

urlpatterns = [
    path('', rides.home, name='home'),
    path('r/', include(([
        path('', rider.SetLocation.as_view(), name='book'),
        path('live/', rider.BookRide.as_view(), name='live'),
        path('rides/', rider.PastRides.as_view(), name='history'),
    ], 'rides'), namespace='rider')),
    path('e/', include(([
        path('live/', executive.RideAlert.as_view(), name='alerts'),
        path('rides/', executive.PastRides.as_view(), name='history'),
        path('payments/', executive.Payments.as_view(), name='payments'),
        path('history/', executive.PastRides.as_view(), name='history'),
        path('maps/', executive.Maps.as_view(), name='maps')
    ], 'rides'), namespace='exec')),
]

