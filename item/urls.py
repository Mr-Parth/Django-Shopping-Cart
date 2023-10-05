from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('api/add_item/',add_item),
    path('api/add_items/',add_items_bulk),
    path('api/edit_item/<int:item_id>',edit_item),
    path('api/delete_item/<int:item_id>',delete_item),
]
