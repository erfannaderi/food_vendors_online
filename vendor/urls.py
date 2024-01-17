from django.urls import path, include
from accounts.views import restaurant_dashboard
from vendor.views import restaurant_profile, menu_builder

urlpatterns = [
    path('', restaurant_dashboard, name='restaurant'),
    path('profile', restaurant_profile, name='restaurant_profile'),
    path('menu-builder', menu_builder, name='menu_builder'),
]
