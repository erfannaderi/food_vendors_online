from django import forms

from vendor.models import Vendor


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', "vendor_license"]
        # verbose_name = "Vendor"
        # verbose_name_plural = "Vendors"
