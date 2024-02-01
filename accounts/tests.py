# accounts/tests.py
from django.test import TestCase
from accounts.models import User, Address


class UserTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="johndoe@example.com",
            password="password123"
        )
        self.assertEqual(user.username, "johndoe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            first_name="Admin",
            last_name="User",
            username="adminuser",
            email="admin@example.com",
            password="superpassword123"
        )
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class AddressTestCase(TestCase):
    def test_address_creation(self):
        user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="johndoe@example.com",
            password="password123"
        )
        address = Address.objects.create(
            user=user,
            address="123 Main St",
            country="USA",
            state="CA",
            city="Los Angeles",
            pin_code="90001",
            latitude="34.0522",
            longitude="118.2437"
        )
        self.assertEqual(address.user.email, "johndoe@example.com")
        self.assertEqual(address.country, "USA")
