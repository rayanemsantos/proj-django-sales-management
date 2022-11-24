from django.test import TestCase
from customer.models import Customer


class SetupData:
    def create_customer(self):
        self.customer = Customer.objects.create(
            name='Rayane Maria',
            email='rayanemsantos.contato@gmail.com',
            phone='85986204006'
        )


class CustomerTestCase(TestCase):
    start = SetupData()

    def setUp(self):
        self.start.create_customer()

    def test_get(self):
        customer = Customer.objects.first()
        self.assertIsInstance(customer, Customer)

    def test_update(self):
        customer = Customer.objects.first()
        customer.name = 'Rayane Maria'
        customer.save()
        self.assertEqual(customer.name, 'Rayane Maria')

    def test_str(self):
        customer = Customer.objects.first()
        self.assertEqual(customer.__str__(), 'Rayane Maria')

    def test_delete(self):
        customer = Customer.objects.first()
        customer.delete()

        self.assertFalse(customer.id)
        self.assertIsInstance(customer, Customer)
