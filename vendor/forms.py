from django import forms

from accounts.models import UserProfile
from accounts.validators import allow_images_only_validator
from vendor.models import Vendor


class RestaurantForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
                                     validators=[allow_images_only_validator])

    class Meta:
        model = Vendor
        fields = ['vendor_name', "vendor_license"]
        # verbose_name = "Vendor"
        # verbose_name_plural = "Vendors"


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
                                      validators=[allow_images_only_validator])
    # we can use ImageField instead of FileField for django automatic
    # validation, but since we have custom validation, we use the FileField
    cover_photos = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
                                   validators=[allow_images_only_validator])

    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly' : 'readonly'}))
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly' : 'readonly'}))

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photos', 'address', 'country', 'state', 'city',
                  'pin_code', 'latitude', 'longitude', ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
