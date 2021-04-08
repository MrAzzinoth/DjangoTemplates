from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='signup'),
    path('signup/', SignInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
]

