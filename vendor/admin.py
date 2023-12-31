from django.contrib import admin
from vendor.models import Vendor


# Register your models here.
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    date_hierarchy = 'modified_at'
    empty_value_display = "-empty-"

# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ["name", "title", "view_birth_date"]
#
#     @admin.display(empty_value="???")
#     def view_birth_date(self, obj):
#         return obj.birth_date
