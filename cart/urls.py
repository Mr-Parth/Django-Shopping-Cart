from django.contrib import admin
from django.urls import path
from cart.views import *

urlpatterns = [
    path('add-item/<int:item_id>', add_to_cart),
    path('remove-item/<int:item_id>', remove_from_cart),
    path('list-items/', list_user_cart_items)
]
