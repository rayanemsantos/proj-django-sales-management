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

        self.sale = Sale.objects.create(
            access_key='35210822910629000101550090004001241944828331',
            seller=Seller.objects.first(),
            customer=Customer.objects.first()
        )

    def create_sale_product(self):
        product_setup = ProductSetupData()
        product_setup.create_product()

        self.sale_product = SaleProduct.objects.create(
            sale=Sale.objects.first(),
            product=Product.objects.first(),
            quantity=2
        )


class SaleTestCase(TestCase):
    start = SetupData()

    def setUp(self):
        self.start.create_sale()

    def test_get(self):
        sale = Sale.objects.first()
        self.assertIsInstance(sale, Sale)

    def test_update(self):
        sale = Sale.objects.first()
        sale.access_key = '35210822910629000101550090004001241944828632'
        sale.save()
        self.assertEqual(
            sale.access_key, '35210822910629000101550090004001241944828632')

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

    def test_str(self):
        sale_product = SaleProduct.objects.first()
        self.assertEqual(sale_product.__str__(), "{} x {}".format(
            sale_product.product.description, sale_product.quantity))

    def test_delete(self):
        sale_product = SaleProduct.objects.first()
        sale_product.delete()

        self.assertFalse(sale_product.id)
        self.assertIsInstance(sale_product, SaleProduct)
