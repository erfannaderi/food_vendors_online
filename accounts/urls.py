from django.urls import path
from .views import RegisterClientView, RegisterRestaurantView

# /accounts/regeister-client/
urlpatterns = [
    path('regeister-client/', RegisterClientView.as_view(), name='register_client'),
    path('regeister-restaurant/', RegisterRestaurantView.as_view(), name='register_restaurant'),
]
