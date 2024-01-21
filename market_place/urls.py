from django.urls import path

from market_place.views import MarketPlaceView, RestaurantDetailView

urlpatterns = [
    path('', MarketPlaceView.as_view(), name='market_place'),
    path('<slug:vendor_slug>', RestaurantDetailView.as_view(), name='restaurant_detail_view'),

]
