from django.urls import path

from accounts.views import RegisterClientView, RegisterRestaurantView

# from .views import RegisterClientView, RegisterRestaurantView

# /accounts/register-client/
urlpatterns = [
    path('register-client/', RegisterClientView.as_view(), name='register_client'),
    path('register-restaurant/', RegisterRestaurantView.as_view(), name='register_restaurant'),
]
