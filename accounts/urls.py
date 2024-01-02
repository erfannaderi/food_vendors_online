from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import RegisterClientView, register_restaurant, MyLoginView

# from .views import RegisterClientView, RegisterRestaurantView

# /accounts/register-client/
urlpatterns = [
    path('register-client/', RegisterClientView.as_view(), name='register_client'),
    path('register-restaurant/', register_restaurant, name='register_restaurant'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # path('dashboard/', dashboard, name='dashboard'),
]
