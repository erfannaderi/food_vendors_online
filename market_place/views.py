from django.db.models import Prefetch
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from menu.models import Category, FoodItem
from vendor.models import Vendor


# Create your views here.
class MarketPlaceView(ListView):
    model = Vendor
    template_name = 'marketplace/listings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
        vendor_counter = vendors.count()
        context['vendors'] = vendors
        context['vendors_counter'] = vendor_counter
        return context


class RestaurantDetailView(DetailView):
    model = Vendor
    template_name = 'marketplace/detail.html'
    context_object_name = 'vendor'  # Set the context object name to 'vendor'

    def get_object(self, queryset=None):
        vendor_slug = self.kwargs.get('vendor_slug')
        vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
        return vendor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = self.get_object()
        categories = Category.objects.filter(vendor=vendor).prefetch_related(
            Prefetch(
                'fooditems',
                queryset= FoodItem.objects.filter(is_available=True)
            )
        )
        context['categories'] = categories
        return context

