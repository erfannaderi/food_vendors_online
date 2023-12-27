from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, UserProfile


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'first_name', 'last_name')
    ordering = ('-created_date',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile,)

