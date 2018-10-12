from django.contrib import admin
from django.urls import path, include
from .views import homeView, UserView, testApi, registerUser, checkUserExists, create_fb_user


urlpatterns = [
    path('', testApi),
    path('user/', UserView.as_view()),
    path('user/<int:user_id>/', UserView.as_view()),
    path('user/registeruser/', registerUser),
    path('test/', testApi),
    path('checkuser/',checkUserExists),
    path('createfbuser/', create_fb_user)
]
