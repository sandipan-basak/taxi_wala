from django.urls import path, include
from .views import rides, executive, rider


urlpatterns = [
    path('', rides.home, name='home'),

    path('r/', include(([
        path('', rider.SetLocation.as_view(), name='book'),
        path('live/<int:pk>', rider.BookRide.as_view(), name='live'),
        # path('/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('status/', rider.RideView.as_view(), name='status'),
        path('rides/', rider.PastRides.as_view(), name='history'),
    ], 'rides'), namespace='rider')),
    path('e/', include(([
        path('live/', executive.RideAlert.as_view(), name='alerts'),
        path('payments/', executive.Payments.as_view(), name='payments'),
        path('history/', executive.Rides.as_view(), name='history'),
        path('maps/', executive.Maps.as_view(), name='maps')
    ], 'rides'), namespace='exec')),
]

