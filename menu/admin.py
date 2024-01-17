from django.contrib import admin

from menu.models import FoodItem, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(FoodItem)
