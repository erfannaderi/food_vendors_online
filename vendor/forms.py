from django import forms

from accounts.models import Address, User
# from accounts.validators import allow_images_only_validator
from vendor.models import Vendor, OpeningHours


class RestaurantForm(forms.ModelForm):
    vendor_license = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))

    class Meta:
        model = Vendor
        fields = ['vendor_name', "vendor_license"]
        # verbose_name = "Vendor"
        # verbose_name_plural = "Vendors"


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    # we can use ImageField instead of FileField for django automatic
    # validation, but since we have custom validation, we use the FileField
    cover_photos = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))

    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly' : 'readonly'}))
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly' : 'readonly'}))

    class Meta:
        model = User
        fields = ['profile_picture', 'cover_photos', 'address']


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(UserAddressForm, self).__init__(*args, **kwargs)  # Fixed the super call
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ['day', 'from_hours', 'to_hours', 'is_closed']
