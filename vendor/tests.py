# vendors/tests.py
from django.test import TestCase
from datetime import time, datetime, date
from accounts.models import User
from vendor.models import Vendor, OpeningHours, Staff


class VendorTestCase(TestCase):
    def test_vendor_creation(self):
        user = User.objects.create(username="testvendor", email="testvendor@example.com")
        vendor = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        self.assertEqual(vendor.vendor_name, "Test Vendor")
        self.assertEqual(vendor.vendor_slug, "test-vendor")

    def test_is_open(self):
        user = User.objects.create(username="testvendor", email="testvendor@example.com")
        vendor = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        opening_hours = OpeningHours.objects.create(vendor=vendor, day=1, from_hours="09:00 AM", to_hours="05:00 PM", is_closed=False)
        # Add more opening hours for testing different scenarios
        self.assertTrue(vendor.is_open())

class StaffTestCase(TestCase):
    def test_staff_creation(self):
        user = User.objects.create(username="staffuser", email="staffuser@example.com")
        vendor = Vendor.objects.create(user=user, vendor_name="Test Vendor", vendor_slug="test-vendor")
        staff = Staff.objects.create(user=user, vendor=vendor, role=Staff.ROLE_MANAGER)
        self.assertEqual(staff.user.username, "staffuser")
        self.assertEqual(staff.get_role_display(), "Manager")
