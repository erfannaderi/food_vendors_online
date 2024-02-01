from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from menu.models import FoodItem
from online_food.models import BaseModel


# Create your models here.
class Discount(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    discount_code = models.CharField(max_length=50)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Discount Percentage (%)')
    minimum = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    maximum = models.DecimalField(max_digits=12, decimal_places=2, default=800)
    start_date = models.DateField()
    counter = models.IntegerField(default=0)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Discount ({self.discount_code})"


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user


class Tax(BaseModel):
    tax_type = models.CharField(max_length=20, unique=True, db_index=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Tax Percentage (%)')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('tax')
        verbose_name_plural = _('taxes')

    def __str__(self):
        return self.tax_type
