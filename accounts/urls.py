from django.urls import path

from accounts.views import RegisterClientView, register_restaurant

# from .views import RegisterClientView, RegisterRestaurantView

# /accounts/register-client/
urlpatterns = [
    path('register-client/', RegisterClientView.as_view(), name='register_client'),
    path('register-restaurant/', register_restaurant, name='register_restaurant'),
]
