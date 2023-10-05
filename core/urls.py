from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path('user/login/', login_user),
    path('user/register/', register_user),
    path('user/suspend-user/<int:user_id>', suspend_user)
]
