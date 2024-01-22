from market_place.models import Cart

def get_cart_counter(request):
    cart_count = 0

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

        if cart_items:
            for cart_item in cart_items:
                cart_count += cart_item.quantity

    return dict(cart_counter=cart_count)