from django.urls import path, include
from accounts.views import restaurant_dashboard, my_account
from menu.views import food_category_add, food_items_by_category, menu_builder, food_category_update, \
    food_category_delete, food_item_add, food_item_update, food_item_delete
from vendor.views import restaurant_profile

urlpatterns = [
    path('', restaurant_dashboard, name='restaurant'),
    path('profile', restaurant_profile, name='restaurant_profile'),
    path('menu-builder', menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', food_items_by_category, name='food_items_by_category'),
    # category CRUD
    path('menu-builder/category/add/', food_category_add, name='food_category_add'),
    path('menu-builder/category/', my_account, name='my_account'),
    path('menu-builder/category/update/<int:pk>', food_category_update, name='food_category_update'),
    path('menu-builder/category/delete/<int:pk>', food_category_delete, name='food_category_delete'),
    # food items crud
    path('menu-builder/food-item/add/', food_item_add, name='food_item_add'),
    path('menu-builder/food-item/', my_account, name='my_account'),
    path('menu-builder/', my_account, name='my_account'),
    path('menu-builder/food-item/update/<int:pk>', food_item_update, name='food_item_update'),
    path('menu-builder/food-item/delete/<int:pk>', food_item_delete, name='food_item_delete'),
]
