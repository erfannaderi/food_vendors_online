from django.urls import path

from market_place.views import MarketPlaceView, RestaurantDetailView, add_to_cart_view, decrease_cart_view, \
    delete_cart_view

urlpatterns = [
    path('', MarketPlaceView.as_view(), name='market_place'),
    path('<slug:vendor_slug>', RestaurantDetailView.as_view(), name='restaurant_detail_view'),
    # cart crud
    path('add-to-cart/<int:food_item_pk>/', add_to_cart_view, name='add_to_cart'),
    path('decrease-cart/<int:food_item_pk>/', decrease_cart_view, name='decrease_cart'),
    path('delete-cart/<int:food_item_pk>/', delete_cart_view, name='delete_cart'),

]
