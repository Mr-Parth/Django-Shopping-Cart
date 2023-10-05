from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('add_item/',add_item),
    path('add_items/',add_items_bulk),
    path('edit_item/<int:item_id>',edit_item),
    path('delete_item/<int:item_id>',delete_item),
]
