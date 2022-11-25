import json
import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from customer.models import Customer
from seller.models import Seller
from product.models import Product
from sale.models import Sale

from sale.tests.tests_models import SetupData as SaleSetup


class SaleViewSetTestCase(TestCase):

    def setUp(self):
        self.sale_setup = SaleSetup()

        self.sale_setup.create_sale()
        self.sale_setup.create_sale_product()

        self.client = APIClient()

        self.base_route = '/api/sale'

    def test_list(self):
        response = self.client.get(self.base_route, follow=True)
        data = response.json()
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(type(data) == list)

    def test_get_object(self):
        sale = Sale.objects.first()
        response = self.client.get(
            self.base_route + '/' + str(sale.id), follow=True)
        data = response.json()
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(type(data) == dict)

    def test_post(self):
        payload = {
            "seller": Seller.objects.first().id,
            "customer": Customer.objects.first().id,
            "access_key": "35210822910629000101550090004001241944828631",
            "products": [{"product": Product.objects.first().id, "quantity": 2}]
        }

        response = self.client.post(
            self.base_route + '/', data=payload, follow=True, format="json")

        self.assertTrue(
            len(response.data['sale_products']) == len(payload['products']))
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in response.json())

    def test_put(self):
        sale = Sale.objects.first()
        sale_products = sale.saleproduct_set.all()

        products = []

        for _product in sale_products:
            products.append({
                "id": _product.id,
                "product": _product.product.id,
                "quantity": _product.quantity
            })
            products.append({
                "product": _product.product.id,
                "quantity": 2
            })

        payload = {
            "seller": sale.seller.id,
            "customer": sale.customer.id,
            "access_key": "387454938759384759823759875984",
            "products": products
        }

        response = self.client.put(
            self.base_route + '/' + str(sale.id) + '/', data=payload, follow=True, format="json")

        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(
            len(response.data['sale_products']) == len(payload['products']))
        self.assertTrue("id" in response.json())

    def test_delete(self):
        sale = Sale.objects.last()
        response = self.client.delete(
            self.base_route + '/' + str(sale.id) + '/')
        self.assertTrue(status.is_success(response.status_code))


class SaleCommissionsViewSetCase(TestCase):

    def setUp(self):
        self.sale_setup = SaleSetup()

        self.sale_setup.create_sale()
        self.sale_setup.create_sale_product()

        self.client = APIClient()

        self.base_route = '/api/sale_commissions'

    def test_list(self):
        today = datetime.datetime.today()
        day_init = today.replace(hour=0, minute=0, second=0)
        day_end = today.replace(hour=23, minute=59, second=59)
        init_format = day_init.strftime('%Y-%m-%d')
        end_format = day_end.strftime('%Y-%m-%d')

        query = '/?date_init=' + init_format + '&' + 'date_end=' + end_format
        response = self.client.get(self.base_route + query, follow=True)
        data = response.json()

        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("results" in data)
        self.assertTrue(type(data["results"]) == list)
        self.assertTrue("total" in data)
