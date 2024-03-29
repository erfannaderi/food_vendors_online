from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Address


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'first_name', 'last_name')
    ordering = ('-created_date',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'country', 'state', 'city')


admin.site.register(Address, AddressAdmin)

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     # Define the fields to be displayed in the admin interface
#     # list_display = ('user', 'date_of_birth', 'phone_number', 'address')
#     pass
