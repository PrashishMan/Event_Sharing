from django.contrib import admin
from django.urls import path
from .views import testApi
from django.conf.urls import url

from .views import login_user

from rest_framework.authtoken import views
from .views import CustomAuthToken



urlpatterns = [
    path('login/', login_user),
    url(r'^api-token-auth/', CustomAuthToken.as_view())

]
