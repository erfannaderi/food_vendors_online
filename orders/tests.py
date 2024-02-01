from django.test import TestCase
from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor
from .models import Payment, Order, OrderedFood


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.vendor = Vendor.objects.create(vendor_name='Test Vendor',
                                            user=self.user)  # Associate the user with the vendor
        self.food_item = FoodItem.objects.create(food_title='Test Food', price=10.0)
        self.payment = Payment.objects.create(user=self.user, transaction_id='12345', payment_method='PayPal',
                                              amount='10.0', status='Success')
        self.order = Order.objects.create(
            user=self.user,
            payment=self.payment,
            order_number='123',
            first_name='John',
            last_name='Doe',
            phone='123456789',
            email='john@example.com',
            address='Test Address',
            city='Test City',
            pin_code='12345',
            total=10.0,
            total_tax=1.0,
            payment_method='PayPal',
            status='New'
        )
        self.ordered_food = OrderedFood.objects.create(
            order=self.order,
            payment=self.payment,
            user=self.user,
            fooditem=self.food_item,
            quantity=2,
            price=10.0,
            amount=20.0
        )


def test_payment_model(self):
    payment = Payment.objects.get(transaction_id='12345')
    self.assertEqual(payment.user, self.user)
    self.assertEqual(payment.payment_method, 'PayPal')
    self.assertEqual(payment.amount, '10.0')
    self.assertEqual(payment.status, 'Success')


def test_order_model(self):
    order = Order.objects.get(order_number='123')
    self.assertEqual(order.user, self.user)
    self.assertEqual(order.payment, self.payment)
    self.assertEqual(order.first_name, 'John')
    self.assertEqual(order.last_name, 'Doe')
    self.assertEqual(order.phone, '123456789')
    self.assertEqual(order.email, 'john@example.com')
    self.assertEqual(order.address, 'Test Address')
    self.assertEqual(order.city, 'Test City')
    self.assertEqual(order.pin_code, '12345')
    self.assertEqual(order.total, 10.0)
    self.assertEqual(order.total_tax, 1.0)
    self.assertEqual(order.payment_method, 'PayPal')
    self.assertEqual(order.status, 'New')


def test_ordered_food_model(self):
    ordered_food = OrderedFood.objects.get(fooditem=self.food_item)
    self.assertEqual(ordered_food.order, self.order)
    self.assertEqual(ordered_food.payment, self.payment)
    self.assertEqual(ordered_food.user, self.user)
    self.assertEqual(ordered_food.fooditem, self.food_item)
    self.assertEqual(ordered_food.quantity, 2)
    self.assertEqual(ordered_food.price, 10.0)
    self.assertEqual(ordered_food.amount, 20.0)
