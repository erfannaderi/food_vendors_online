from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from market_place.context_processors import get_cart_counter, get_cart_amount
from market_place.models import Cart
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
                queryset=FoodItem.objects.filter(is_available=True)
            )
        )
        if self.request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=self.request.user)
        else:
            cart_items = None

        context['categories'] = categories
        context['cart_items'] = cart_items
        return context


def add_to_cart_view(request, food_item_pk):
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # check if food exists
            try:
                food_item = get_object_or_404(FoodItem, pk=food_item_pk, is_available=True)
                # check if already added to the cart
                try:
                    check_cart = Cart.objects.get(user=request.user, food_item=food_item)
                    # increase quantity of food item
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse(
                        {'status': 'success', 'message': 'Added extra one', 'cart_counter': get_cart_counter(request),
                         'qty': check_cart.quantity, 'cart_amount': get_cart_amount(request)})
                except:
                    check_cart = Cart.objects.create(user=request.user, food_item=food_item, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'food added to cart',
                                         'cart_counter': get_cart_counter(request), 'qty': check_cart.quantity,
                                         'cart_amount': get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'failed', 'message': 'Invalid request food does not exist'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
    return JsonResponse({'status': 'login_required', 'message': 'please login to continue'})


def decrease_cart_view(request, food_item_pk):
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # check if food exists
            try:
                food_item = FoodItem.objects.get(pk=food_item_pk, is_available=True)
                # check if already added to the cart
                try:
                    check_cart = Cart.objects.get(user=request.user, food_item=food_item)
                    # Decrease quantity of food item or delete
                    if check_cart.quantity > 1:
                        check_cart.quantity -= 1
                        check_cart.save()
                        return JsonResponse(
                            {'status': 'success', 'message': 'Decreased one', 'cart_counter': get_cart_counter(request),
                             'qty': check_cart.quantity, 'cart_amount': get_cart_amount(request)})
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                        return JsonResponse(
                            {'status': 'success', 'message': 'you do not have this item',
                             'cart_counter': get_cart_counter(request),
                             'qty': check_cart.quantity, 'cart_amount': get_cart_amount(request)})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'you do not have this item'})
            except:
                return JsonResponse({'status': 'failed', 'message': 'Invalid request food does not exist'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
    return JsonResponse({'status': 'login_required', 'message': 'please login to continue'})


def delete_cart_view(request, food_item_pk):
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # check if food exists
            try:
                food_item = get_object_or_404(FoodItem, pk=food_item_pk, is_available=True)
                # check if already added to the cart
                try:
                    check_cart = Cart.objects.get(user=request.user, food_item=food_item)
                    check_cart.delete()
                    return JsonResponse(
                        {'status': 'success', 'message': 'Item removed from cart',
                         'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amount(request)}
                    )
                except Cart.DoesNotExist:
                    return JsonResponse({'status': 'failed', 'message': 'Item not found in cart'})
            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'failed', 'message': 'Invalid food item'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
    return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


@login_required(login_url='login')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def search_view(request):
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']
    fetch_vendors_by_food_items = FoodItem.objects.filter(food_title__icontains=keyword,
                                                          is_available=True).values_list('vendor', flat=True)
    vendors = Vendor.objects.filter(Q(pk__in=fetch_vendors_by_food_items) |
                                    Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
    print(fetch_vendors_by_food_items)
    # vendors = Vendor.objects.filter(vendor_name__icontains=keyword, is_approved=True, user__is_active=True)
    vendor_counter = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_counter': vendor_counter,
    }
    return render(request, 'marketplace/listings.html', context)
