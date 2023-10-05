from django.contrib import admin
from django.urls import path
from cart.views import *

urlpatterns = [
    path('add_item/<str:product_name>', add_to_cart),
    path('remove_item/<str:product_name>', remove_from_cart),
    path('list_items/', list_user_cart_items)
]
