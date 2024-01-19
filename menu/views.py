from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify

from accounts.views import check_role_vendor
from menu.forms import CategoryMenuForm, FoodItemForm
from menu.models import Category, FoodItem
from vendor.views import get_vendor


# Create your views here.

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    # filter for more than one specific object
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('category_name')
    context = {
        "categories": categories
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def food_items_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    food_items = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        "category": category,
        'food_items': food_items
    }
    return render(request, 'vendor/food_items_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def food_category_add(request):
    if request.method == 'POST':
        form = CategoryMenuForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category has been added")
            return redirect('menu_builder')
    else:
        form = CategoryMenuForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/food_category_add.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def food_category_update(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryMenuForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category has been updated successfully")
            return redirect('menu_builder')
    else:
        form = CategoryMenuForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/food_category_update.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def food_category_delete(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.warning(request, "Category successfully deleted")
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def food_item_add(request):
    if request.method == 'POST':
        form = CategoryMenuForm(request.POST)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food_item = form.save(commit=False)
            food_item.vendor = get_vendor(request)
            food_item.slug = slugify(food_title)
            form.save()
            messages.success(request, "Category has been added")
            return redirect('menu_builder')
    else:
        form = FoodItemForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/food_item_add.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def food_item_update(request, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = CategoryMenuForm(request.POST, instance=food_item)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food_item = form.save(commit=False)
            food_item.vendor = get_vendor(request)
            food_item.slug = slugify(food_title)
            form.save()
            messages.success(request, "food item has been updated successfully")
            return redirect('menu_builder')
    else:
        form = CategoryMenuForm(instance=food_item)
    context = {
        'form': form,
        'category': food_item,
    }
    return render(request, 'vendor/food_item_update.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def food_item_delete(request, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    food_item.delete()
    messages.warning(request, "Food item successfully deleted")
    return redirect('menu_builder')
