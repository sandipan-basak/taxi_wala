from django.urls import path, include
from .views import rides, executive, rider


urlpatterns = [
    path('', rides.home, name='home'),

    path('r/', include(([
        path('', rider.BookRideView.as_view(), name='book'),
        path('status/', rider.RideStatusView.as_view(), name='status'),
    ], 'rides'), namespace='rider')),

    path('e/', include(([
        path('live/', executive.Ride_Alert.as_view(), name='alerts'),
        path('payments/', executive.PaymentsView.as_view(), name='payments'),
    ], 'rides'), namespace='exec')),
]


# Be careful setting the name to just /login use userlogin instead!
# urlpatterns=[
#     path('register/',views.register,name='register'),
#     path('user_login/',views.user_login,name='user_login'),
# ]
