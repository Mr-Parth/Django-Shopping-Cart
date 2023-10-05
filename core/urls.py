from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path('login/', login_user),
    path('register/', register_user),
    path('suspend_user/<int:user_id>', suspend_user)
]
