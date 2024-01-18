from django.urls import path, include
from accounts.views import restaurant_dashboard
from menu.views import food_category_add, food_items_by_category, menu_builder
from vendor.views import restaurant_profile

urlpatterns = [
    path('', restaurant_dashboard, name='restaurant'),
    path('profile', restaurant_profile, name='restaurant_profile'),
    path('menu-builder', menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', food_items_by_category, name='food_items_by_category'),
    # category CRUD
    path('menu-builder/category/add/', food_category_add, name='food_category_add'),

]
