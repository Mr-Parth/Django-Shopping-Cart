from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path('user/login/', login),
    path('user/register/', register),
    path('suspend-user/', suspend_user),
    path('add-items/',add_item),
]
