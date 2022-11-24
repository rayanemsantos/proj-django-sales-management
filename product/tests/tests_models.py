from django.test import TestCase
from django.core.exceptions import ValidationError

from product.models import Product, ProductCommissionSchedule


class SetupData:
    def create_product(self):
        self.product = Product.objects.create(
            code=1,
            description='Mouse Logitech',
            unit_price=59.99,
            commission_percentage=10,
        )

    def create_product_commission_schedule(self):
        self.commission_schedule = ProductCommissionSchedule.objects.create(
            product=Product.objects.first(),
            day_week=1,
            min_percentage=3,
            max_percentage=8
        )


class ProductTestCase(TestCase):
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


class ProductCommissionScheduleTestCase(TestCase):
    start = SetupData()

    def setUp(self):
        self.start.create_product()
        self.start.create_product_commission_schedule()

    def test_commission_validation(self):
        commission_schedule = ProductCommissionSchedule.objects.first()
        commission_schedule.full_clean()
        commission_schedule.min_percentage = 11
        commission_schedule.max_percentage = 11
        self.assertRaises(ValidationError, commission_schedule.full_clean)

    def test_get(self):
        commission_schedule = ProductCommissionSchedule.objects.first()
        self.assertIsInstance(commission_schedule, ProductCommissionSchedule)

    def test_update(self):
        commission_schedule = ProductCommissionSchedule.objects.first()
        commission_schedule.min_percentage = 4
        commission_schedule.save()
        self.assertEqual(commission_schedule.min_percentage, 4)

    def test_str(self):
        commission_schedule = ProductCommissionSchedule.objects.first()
        self.assertEqual(commission_schedule.__str__(),
                         'Segunda-feira - Mouse Logitech')

    def test_delete(self):
        commission_schedule = ProductCommissionSchedule.objects.first()
        commission_schedule.delete()

        self.assertFalse(commission_schedule.id)
        self.assertIsInstance(commission_schedule, ProductCommissionSchedule)
