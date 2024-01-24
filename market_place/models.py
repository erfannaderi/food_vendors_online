from django.db import models

from accounts.models import User
from menu.models import FoodItem


# Create your models here.
class Discount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount_code = models.CharField(max_length=50)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Discount Percentage (%)')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Discount ({self.discount_code})"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user


class Tax(models.Model):
    tax_type = models.CharField(max_length=20, unique=True, db_index=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Tax Percentage (%)')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'tax'
        verbose_name_plural = 'taxes'

    def __str__(self):
        return self.tax_type
