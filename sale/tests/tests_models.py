import datetime
from django.test import TestCase
from sale.models import Sale, SaleProduct
from product.models import Product
from customer.models import Customer
from seller.models import Seller

from product.tests.tests_models import SetupData as ProductSetupData
from seller.tests.tests_models import SetupData as SellerSetup
from customer.tests.tests_models import SetupData as CustomerSetup


class SetupData:
    def create_sale(self):
        self.seller_setup = SellerSetup()
        self.customer_setup = CustomerSetup()
        self.seller_setup.create_seller()
        self.customer_setup.create_customer()

        self.sale = Sale.objects.create(
            access_key='35210822910629000101550090004001241944828631',
            seller=Seller.objects.first(),
            customer=Customer.objects.first(),
        )

    def create_sale_product(self):
        product_setup = ProductSetupData()
        sale = Sale.objects.first()
        day_week_today = datetime.datetime.today().weekday() + 1

        # product 1
        product_with_schedule = product_setup.create_product()
        product_setup.create_product_commission_schedule(product=product_with_schedule, day_week=day_week_today)

        # product 2
        product_without_schedule = product_setup.create_product(2, 'SSD 1TB', 1190.99, 10)

        # product 3
        product_with_schedule_2 = product_setup.create_product(3, 'SSD 500GB', 990.99, 2)
        product_setup.create_product_commission_schedule(product=product_with_schedule_2, day_week=day_week_today + 1)

        self.saleproduct_1 = SaleProduct.objects.create(
            sale=sale,
            product=product_with_schedule,
            quantity=2
        )

        self.saleproduct_2 = SaleProduct.objects.create(
            sale=sale,
            product=product_without_schedule,
            quantity=3
        )

        self.saleproduct_3 = SaleProduct.objects.create(
            sale=sale,
            product=product_with_schedule_2,
            quantity=3
        )


class SaleTestCase(TestCase):
    start = SetupData()

    def setUp(self):
        self.start.create_sale()
        self.start.create_sale_product()

    def test_get(self):
        sale = Sale.objects.first()
        self.assertIsInstance(sale, Sale)

    def test_update(self):
        sale = Sale.objects.first()
        sale.access_key = '35210822910629000101550090004001241944828632'
        sale.save()
        self.assertEqual(
            sale.access_key, '35210822910629000101550090004001241944828632')

    def test_change_total_after_delete_sale_product(self):
        sale = Sale.objects.first()
        previous_total = sale.total
        sale.saleproduct_set.last().delete()
        current_total = sale.total
        self.assertTrue(previous_total > current_total)

    def test_str(self):
        sale = Sale.objects.first()
        self.assertEqual(sale.__str__(), '# {}'.format(sale.id))

    def test_delete(self):
        sale = Sale.objects.first()
        sale.delete()

        self.assertFalse(sale.id)
        self.assertIsInstance(sale, Sale)


class SaleProductTestCase(TestCase):
    start = SetupData()

    def setUp(self):
        self.start.create_sale()
        self.start.create_sale_product()

    def test_get(self):
        sale_product = SaleProduct.objects.first()
        self.assertIsInstance(sale_product, SaleProduct)

    def test_update(self):
        sale_product = SaleProduct.objects.first()
        sale_product.quantity = 3
        sale_product.save()
        self.assertEqual(
            sale_product.quantity, 3)

    def test_change_total_after_alter_quantity(self):
        sale_product = SaleProduct.objects.first()
        sale_product.quantity = 4
        previous_total = sale_product.total
        sale_product.save()
        current_total = sale_product.total

        self.assertTrue(previous_total != current_total)

    def test_commission_applied_without_schedule(self):
        saleproduct = self.start.saleproduct_2
        self.assertEqual(saleproduct.commission_applied, 10)

    def test_commission_applied_with_schedule(self):
        saleproduct = self.start.saleproduct_1
        self.assertEqual(saleproduct.commission_applied, 8)

    def test_commission_applied_with_schedule_not_valid_for_today(self):
        saleproduct = self.start.saleproduct_3
        self.assertEqual(saleproduct.commission_applied, 2)

    def test_str(self):
        sale_product = SaleProduct.objects.first()
        self.assertEqual(sale_product.__str__(), "{} x {}".format(
            sale_product.product.description, sale_product.quantity))

    def test_delete(self):
        sale_product = SaleProduct.objects.first()
        sale_product.delete()

        self.assertFalse(sale_product.id)
        self.assertIsInstance(sale_product, SaleProduct)
