from django.test import TestCase
from datetime import date, timedelta
from vendor.models import Vendor
from .models import Discount, Cart, Tax
from accounts.models import User
from menu.models import FoodItem, Category


class DiscountTestCase(TestCase):
    def test_discount_creation(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")
        discount = Discount.objects.create(user=user, discount_code="TESTCODE", discount_percentage=10,
                                           start_date=date.today(), end_date=date.today() + timedelta(days=30))
        self.assertEqual(discount.discount_code, "TESTCODE")
        self.assertEqual(discount.discount_percentage, 10)

    def test_discount_counter_increment(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")
        discount = Discount.objects.create(user=user, discount_code="TESTCODE", discount_percentage=10,
                                           start_date=date.today(), end_date=date.today() + timedelta(days=30))
        discount.counter += 1
        discount.save()
        self.assertEqual(discount.counter, 1)

    def test_discount_expired(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")
        expired_discount = Discount.objects.create(user=user, discount_code="EXPIRED", discount_percentage=15,
                                                   start_date=date.today() - timedelta(days=30),
                                                   end_date=date.today() - timedelta(days=1))
        active_discount = Discount.objects.create(user=user, discount_code="ACTIVE", discount_percentage=20,
                                                  start_date=date.today(), end_date=date.today() + timedelta(days=30))

        self.assertFalse(date.today() <= expired_discount.end_date)  # Check if the end date has passed
        self.assertTrue(date.today() <= active_discount.end_date)  # Check if the end date is in the future


class CartTestCase(TestCase):
    def test_cart_creation(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")
        vendor_instance = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        category_instance = Category.objects.create(vendor=vendor_instance, category_name="Test Category",
                                                    slug="test-category")
        food_item = FoodItem.objects.create(vendor=vendor_instance, category=category_instance, food_title="Test Food",
                                            slug="test-food", price=10.99)
        cart = Cart.objects.create(user=user, food_item=food_item, quantity=2)
        self.assertEqual(cart.user.username, "testuser")
        self.assertEqual(cart.food_item.food_title, "Test Food")

    def test_cart_with_discount(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")
        vendor_instance = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        category_instance = Category.objects.create(vendor=vendor_instance, category_name="Test Category",
                                                    slug="test-category")
        food_item = FoodItem.objects.create(vendor=vendor_instance, category=category_instance, food_title="Test Food",
                                            slug="test-food", price=10.99)
        discount = Discount.objects.create(user=user, discount_code="TESTCODE", discount_percentage=15,
                                           start_date=date.today(), end_date=date.today() + timedelta(days=30))
        cart = Cart.objects.create(user=user, food_item=food_item, quantity=2, discount=discount)
        self.assertEqual(cart.discount.discount_percentage, 15)

    def test_cart_quantity_update(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")
        vendor_instance = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        category_instance = Category.objects.create(vendor=vendor_instance, category_name="Test Category",
                                                    slug="test-category")
        food_item = FoodItem.objects.create(vendor=vendor_instance, category=category_instance, food_title="Test Food",
                                            slug="test-food", price=10.99)
        cart = Cart.objects.create(user=user, food_item=food_item, quantity=2)
        cart.quantity = 3
        cart.save()
        self.assertEqual(cart.quantity, 3)

    def test_cart_deletion(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")
        vendor_instance = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        category_instance = Category.objects.create(vendor=vendor_instance, category_name="Test Category",
                                                    slug="test-category")
        food_item = FoodItem.objects.create(vendor=vendor_instance, category=category_instance, food_title="Test Food",
                                            slug="test-food", price=10.99)
        cart = Cart.objects.create(user=user, food_item=food_item, quantity=2)
        cart.delete()
        self.assertFalse(Cart.objects.filter(id=cart.id).exists())


class TaxTestCase(TestCase):
    def test_tax_creation(self):
        tax = Tax.objects.create(tax_type="VAT", tax_percentage=7.5)
        self.assertEqual(tax.tax_type, "VAT")
        self.assertEqual(tax.tax_percentage, 7.5)

    def test_tax_deactivation(self):
        tax = Tax.objects.create(tax_type="VAT", tax_percentage=7.5)
        tax.is_active = False
        tax.save()
        self.assertFalse(tax.is_active)

    def test_tax_reactivation(self):
        tax = Tax.objects.create(tax_type="VAT", tax_percentage=7.5)
        tax.is_active = False
        tax.save()
        tax.is_active = True
        tax.save()
        self.assertTrue(tax.is_active)
