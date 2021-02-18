from django.urls import path, include
from .views import rides, executive, rider

# SET THE NAMESPACE!
app_name = 'rides'

urlpatterns = [
    path('', rides.home, name='home'),

    path('r/', include(([
        path('travel/', rider.BoookRideView.as_view(), name='book'),
        # path('/', rider..as_view(), name=''),
    ], 'rides'), namespace='rider')),

    path('e/', include(([
        path('live/', executive.Ride_Alert.as_view(), name='alerts'),
        path('payments/', executive.PaymentsView.as_view(), name='payments'),
    ], 'rides'), namespace='executive')),
]


# Be careful setting the name to just /login use userlogin instead!
# urlpatterns=[
#     path('register/',views.register,name='register'),
#     path('user_login/',views.user_login,name='user_login'),
# ]
