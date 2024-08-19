from django.urls import path 
from .views import login_view

from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard_view, name="dashboard_page"),
    path("signin/", login_view, name="signin_page"),
    path("signout/", logout_view, name="signout_page"),
]
