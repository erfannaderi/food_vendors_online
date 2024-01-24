from django.contrib import admin

from orders.models import Order, Payment, OrderedFood

# Register your models here.
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderedFood)