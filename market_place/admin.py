from django.contrib import admin

from market_place.models import Cart, Discount, Tax


# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'quantity', 'updated_at')


admin.site.register(Cart, CartAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('user', 'discount_percentage', 'discount_code', 'start_date', 'end_date', 'updated_at')


admin.site.register(Discount, DiscountAdmin)


class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')


admin.site.register(Tax, TaxAdmin)
