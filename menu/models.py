from django.db import models
from django.utils.translation import gettext_lazy as _

from online_food.models import BaseModel
from vendor.models import Vendor


# Create your models here.
class Category(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, verbose_name=_('Category Name'))
    description = models.TextField(max_length=250, blank=True, verbose_name=_('Description'))
    slug = models.SlugField(max_length=100, unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                                        related_name='child_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.category_name

    # added to make sure integrity errors for same name different letters are not possible
    def clean(self):
        self.category_name = self.category_name.capitalize()


class RawItem(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Raw Item Name')
    description = models.TextField(max_length=250, blank=True, verbose_name='Description')
    is_deleted = models.BooleanField(default=False)

    # Add other fields related to raw items

    def __str__(self):
        return self.name


class FoodItem(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems')
    food_title = models.CharField(max_length=50, unique=True, verbose_name=_('Food Title'))
    description = models.TextField(max_length=250, blank=True, null=True, verbose_name=_('Description'))
    slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_images')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    raw_items = models.ManyToManyField(RawItem, blank=True)

    class Meta:
        verbose_name = _('food item')
        verbose_name_plural = _('food items')

    def __str__(self):
        return self.food_title
