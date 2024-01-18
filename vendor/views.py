from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import UserProfile
from accounts.views import check_role_vendor
from vendor.forms import RestaurantForm, UserProfileForm
from vendor.models import Vendor


# Create your views here.

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def restaurant_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    restaurant = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        restaurant_form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if profile_form.is_valid() and restaurant_form.is_valid():
            profile_form.save()
            restaurant_form.save()
            messages.success(request, "Profile has been updated")
            return redirect('restaurant_profile')
        else:
            print(profile_form.errors)
            print(restaurant_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        restaurant_form = RestaurantForm(instance=restaurant)
    context = {
        'profile_form': profile_form,
        'restaurant_form': restaurant_form,
        'profile': profile,
        'restaurant': restaurant,
    }
    return render(request, 'vendor/restaurant_profile.html', context)
