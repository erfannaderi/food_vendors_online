from market_place.models import Cart
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count = 0

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

        if cart_items:
            for cart_item in cart_items:
                cart_count += cart_item.quantity

    return dict(cart_counter=cart_count)


def get_cart_amount(request):
    subtotal = 0
    tax = 0
    discount = 0
    total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for cart_item in cart_items:
            food_item = FoodItem.objects.get(pk=cart_item.food_item.pk)
            subtotal += (food_item.price * cart_item.quantity)

        total = subtotal + tax + discount
    return dict(subtotal=subtotal, tax=tax, discount=discount, total=total)
