"""
URL configuration for online_food project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from market_place.views import cart_view, search_view
from online_food.views import HomePageView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', HomePageView.as_view(), name='homepage'),
                  path('', include('accounts.urls')),
                  path('market-place/', include('market_place.urls')),
                  path('', include('allauth.urls')),
                  path('favicon.ico', HomePageView.as_view()),
                  # cart
                  path('cart/', cart_view, name='cart_view'),
                  # search
                  path('search/', search_view, name='search'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
