import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from product.tests.tests_models import SetupData as ProductSetup
from product.models import Product


class ProductViewSetTestCase(TestCase):

    def setUp(self):
        self.start = ProductSetup()
        self.client = APIClient()
        self.start.create_product()
        self.base_route = '/api/product'

    def test_list(self):
        response = self.client.get(self.base_route, follow=True)
        content = json.loads(response.content.decode("utf-8"))
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in content[0])

    def test_get_object(self):
        product = Product.objects.first()
        response = self.client.get(
            self.base_route + '/' + str(product.id), follow=True)
        content = json.loads(response.content.decode("utf-8"))
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in content)

    def test_fail_code_already_used(self):
        product = Product.objects.first()
        payload = {
            'code': product.code,
            'description': 'Mouse Logitech',
            'unit_price': 59.99,
            'commission_percentage': 10
        }
        response = self.client.post(
            self.base_route + '/', data=payload, follow=True, format="json")

        self.assertFalse(status.is_success(response.status_code))

    def test_post(self):
        payload = {
            'code': 3,
            'description': 'Mouse Logitech',
            'unit_price': 59.99,
            'commission_percentage': 10
        }
        response = self.client.post(
            self.base_route + '/', data=payload, follow=True, format="json")

        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in response.json())

    def test_put(self):
        product = Product.objects.first()
        payload = {
            'code': product.code,
            'description': 'Mouse Logitech v2',
            'unit_price': product.unit_price,
            'commission_percentage': product.commission_percentage
        }

        response = self.client.put(
            self.base_route + '/' + str(product.id) + '/', data=payload, follow=True, format="json")

        self.assertTrue(response.data['description'] == payload['description'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in response.json())

    def test_delete(self):
        product = Product.objects.last()
        response = self.client.delete(
            self.base_route + '/' + str(product.id) + '/')
        self.assertTrue(status.is_success(response.status_code))
