from django.urls import path, include
from .views import rides, executive, rider


urlpatterns = [
    path('', rides.home, name='home'),

    path('r/', include(([
        path('', rider.BookRideView.as_view(), name='book'),
        path('status/', rider.RideStatusView.as_view(), name='status'),
        path('rides/', executive.RideView.as_view(), name='history'),
    ], 'rides'), namespace='rider')),

    path('e/', include(([
        path('live/', executive.Ride_Alert.as_view(), name='alerts'),
        path('payments/', executive.PaymentsView.as_view(), name='payments'),
        path('history/', executive.RideView.as_view(), name='history'),

    ], 'rides'), namespace='exec')),
]
