from django.contrib import admin

from market_place.models import Cart, Discount


# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'quantity', 'updated_at')


admin.site.register(Cart, CartAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('user', 'discount_percentage', 'discount_code', 'start_date', 'end_date', 'updated_at')


admin.site.register(Discount, DiscountAdmin)
