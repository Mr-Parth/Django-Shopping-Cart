from django.contrib import admin
from django.urls import path
from cart.views import *

urlpatterns = [
    path('add-item/:item-id', add_to_cart),
    path('remove-item/:item-id', remove_from_cart),
    path('list-items/', list_user_cart_items)
]
