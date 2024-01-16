from django.conf import settings

from vendor.models import Vendor


def get_vendor(request):
    try:
        restaurant = Vendor.objects.get(user=request.user)
    except:
        restaurant = None
    return dict(restaurant=restaurant)


def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}
