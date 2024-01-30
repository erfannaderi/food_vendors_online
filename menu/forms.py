from django import forms

from menu.models import Category, FoodItem


class CategoryMenuForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description', 'parent_category']


class FoodItemForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}))

    class Meta:
        model = FoodItem
        fields = ['category', 'description', 'food_title', 'price', 'image', 'is_available']
