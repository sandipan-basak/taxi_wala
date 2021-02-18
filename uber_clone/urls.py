
from django.contrib import admin
from django.urls import include, path
from rides.views import rides, executive, rider

urlpatterns = [
    path('', include('rides.urls')),
    # path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', rides.SignUpView.as_view(),name='signup'),
    path('accounts/signup/r/', rider.SignUpView.as_view(),name='rider_signup'),
    path('accounts/signup/e/', executive.SignUpView.as_view(),name='executive_signup'),
    # path('accounts/signup/', ),
    # path('accounts/signup/rider', django.contrib.auth.urls),
    # path('accounts/signup/executive', django.contrib.auth.urls),
    #path('rides/', views.index,name=''),
    #path('logout/', views.user_logout, name='logout'),
]