from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import UserProfile
from accounts.views import check_role_vendor
from vendor.forms import RestaurantForm, UserProfileForm, OpeningHoursForm
from vendor.models import Vendor, OpeningHours


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


def opening_hours_views(request):
    opening_hours = OpeningHours.objects.filter(vendor=get_vendor(request))
    form = OpeningHoursForm()
    context = {
        'form': form,
        'opening_hours': opening_hours,
    }
    return render(request, 'vendor/opening_hours_views.html', context)


def add_opening_hours_views(request):
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hours = request.POST.get('from_hours')
            to_hours = request.POST.get('to_hours')
            is_closed = request.POST.get('is_closed')
            try:
                hour = OpeningHours.objects.create(vendor=get_vendor(request), day=day,
                                                   from_hours=from_hours, to_hours=to_hours, is_closed=is_closed)
                if hour:
                    day = OpeningHours.objects.get(pk=hour.pk)
                    if day.is_closed:
                        response = {'status': 'success', 'pk': hour.pk, 'day': day.get_day_display(),
                                    'is_closed': "Closed"}
                    else:
                        response = {'status': 'success', 'pk': hour.pk, 'day': day.get_day_display(),
                                    'from_hours': hour.from_hours, 'to_hours': hour.to_hours}
                return JsonResponse(response)
            except IntegrityError:
                response = {'status': 'failed', "message": from_hours + '-' + to_hours + 'already exists for this day'}
                return JsonResponse(response)
        else:
            pass

    return HttpResponse("Adding opening hours")


def remove_opening_hours_views(request, pk=None):
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHours, pk=pk)
            hour.delete()
            return JsonResponse({'status': 'success', 'pk': pk} )

