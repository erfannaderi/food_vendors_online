# yourapp/tests.py
from django.test import TestCase

from accounts.models import User
from .models import Category, RawItem, FoodItem
from vendor.models import Vendor


class CategoryTestCase(TestCase):
    def test_category_creation(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")  # Create a user
        vendor = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        category = Category.objects.create(vendor=vendor, category_name="Test Category", slug="test-category")
        self.assertEqual(category.category_name, "Test Category")
        self.assertEqual(category.slug, "test-category")

    def test_category_description(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")  # Create a user
        vendor = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        category = Category.objects.create(vendor=vendor, category_name="Test Category", slug="test-category",
                                           description="This is a test category")
        self.assertEqual(category.description, "This is a test category")

    def test_category_parent(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")  # Create a user
        vendor = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        parent_category = Category.objects.create(vendor=vendor, category_name="Parent Category",
                                                  slug="parent-category")
        child_category = Category.objects.create(vendor=vendor, category_name="Child Category", slug="child-category",
                                                 parent_category=parent_category)
        self.assertEqual(child_category.parent_category, parent_category)


class RawItemTestCase(TestCase):
    def test_raw_item_creation(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")  # Create a user
        vendor = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        raw_item = RawItem.objects.create(vendor=vendor, name="Test Raw Item")
        self.assertEqual(raw_item.name, "Test Raw Item")

    def test_raw_item_description(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")  # Create a user
        vendor = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        raw_item = RawItem.objects.create(vendor=vendor, name="Test Raw Item", description="This is a test raw item")
        self.assertEqual(raw_item.description, "This is a test raw item")


class FoodItemTestCase(TestCase):
    def test_food_item_creation(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")  # Create a user
        vendor = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        category = Category.objects.create(vendor=vendor, category_name="Test Category", slug="test-category")
        food_item = FoodItem.objects.create(vendor=vendor, category=category, food_title="Test Food", slug="test-food",
                                            price=10.99)
        self.assertEqual(food_item.food_title, "Test Food")

    def test_food_item_availability(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")  # Create a user
        vendor = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        category = Category.objects.create(vendor=vendor, category_name="Test Category", slug="test-category")
        food_item_available = FoodItem.objects.create(vendor=vendor, category=category, food_title="Available Food",
                                                      slug="available-food", price=5.99, is_available=True)
        food_item_unavailable = FoodItem.objects.create(vendor=vendor, category=category, food_title="Unavailable Food",
                                                        slug="unavailable-food", price=8.99, is_available=False)
        self.assertTrue(food_item_available.is_available)
        self.assertFalse(food_item_unavailable.is_available)
