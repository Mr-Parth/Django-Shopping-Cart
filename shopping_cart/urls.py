from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('core/user/', include('core.urls')),
        path('user/cart/', include('cart.urls')),
        path('item/', include('item.urls')),
    ])),
    
]
