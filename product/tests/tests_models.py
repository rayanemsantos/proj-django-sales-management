from django.test import TestCase
from django.core.exceptions import ValidationError

from product.models import Product


class SetupData:
    def create_product(self):
        self.product = Product.objects.create(
            code=1,
            description='Mouse Logitech',
            unit_price=59.99,
            commission_percentage=10,
        )


class CustomerTestCase(TestCase):
    start = SetupData()

    def setUp(self):
        self.start.create_product()

    def test_commission_validation(self):
        product = Product.objects.first()
        product.full_clean()
        product.commission_percentage = 11
        self.assertRaises(ValidationError, product.full_clean)

    def test_get(self):
        product = Product.objects.first()
        self.assertIsInstance(product, Product)

    def test_update(self):
        product = Product.objects.first()
        product.description = 'Mouse Logitech V2'
        product.save()
        self.assertEqual(product.description, 'Mouse Logitech V2')

    def test_str(self):
        product = Product.objects.first()
        self.assertEqual(product.__str__(), '1 - Mouse Logitech')

    def test_delete(self):
        product = Product.objects.first()
        product.delete()

        self.assertFalse(product.id)
        self.assertIsInstance(product, Product)
