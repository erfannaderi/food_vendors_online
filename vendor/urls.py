from django.urls import path, include
from accounts.views import restaurant_dashboard
from vendor.views import restaurant_profile

urlpatterns = [
    path('', restaurant_dashboard, name='restaurant'),
    path('profile', restaurant_profile, name='restaurant_profile'),
]
