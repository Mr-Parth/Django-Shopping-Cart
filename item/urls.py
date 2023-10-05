from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('add-item/',add_item),
    path('add-items/',add_items_bulk),
    path('edit-item/<int:item_id>',edit_item),
    path('delete-item/<int:item_id>',delete_item),
]
