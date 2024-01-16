from vendor.models import Vendor


def get_vendor(request):
    try:
        restaurant = Vendor.objects.get(user=request.user)
    except:
        restaurant = None
    return dict(restaurant=restaurant)
