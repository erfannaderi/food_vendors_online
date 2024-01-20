# from django.contrib.auth.views import LogoutView
from django.urls import path, include
from accounts.views import RegisterClientView, register_restaurant, MyLoginView, CustomLogoutView, \
    restaurant_dashboard, client_dashboard, my_account, activate, forgot_password, reset_password_validate, \
    reset_password

# from .views import RegisterClientView, RegisterRestaurantView

# /accounts/register-client/
urlpatterns = [
    path('register-client/', RegisterClientView.as_view(), name='register_client'),
    path('register-restaurant/', register_restaurant, name='register_restaurant'),
    path('restaurant-dashboard/', restaurant_dashboard, name='restaurant-dashboard'),
    path('client-dashboard/', client_dashboard, name='client-dashboard'),
    # path('', my_account, name='my_account'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # path('dashboard/', dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('forgot-password', forgot_password, name='forgot_password'),
    path('reset-password_validate/<uidb64>/<token>', reset_password_validate, name='reset_password_validate'),
    path('reset-password', reset_password, name='reset_password'),
    path('restaurant/', include("vendor.urls"))
]
