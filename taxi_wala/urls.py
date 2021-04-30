
from django.contrib import admin
from django.urls import include, path
from rides.views import rides, executive, rider

urlpatterns = [
    path('', include('rides.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', rides.SignUp.as_view(), name='signup'),
    path('accounts/signup/r/', rider.RiderSignUp.as_view(), name='rider_signup'),
    path('accounts/signup/e/', executive.ExecSignUp.as_view(), name='executive_signup'),
    path('admin/', admin.site.urls),
]