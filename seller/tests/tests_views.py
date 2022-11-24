import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from seller.tests.tests_models import SetupData as SellerSetup
from seller.models import Seller


class SellerViewSetTestCase(TestCase):
    token = start = None

    def setUp(self):
        self.start = SellerSetup()
        self.client = APIClient()
        self.start.create_seller()
        self.base_route = '/api/seller'

    def test_list(self):
        response = self.client.get(self.base_route, follow=True)
        content = json.loads(response.content.decode("utf-8"))
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in content[0])

    def test_get_object(self):
        seller = Seller.objects.first()
        response = self.client.get(
            self.base_route + '/' + str(seller.id), follow=True)
        content = json.loads(response.content.decode("utf-8"))
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in content)

    def test_post(self):
        payload = {
            'name': 'José Matias',
            'email': 'josematias@gmail.com',
            'phone': '85986203456'
        }

        response = self.client.post(
            self.base_route + '/', data=payload, follow=True, format="json")

        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in response.json())

    def test_put(self):
        seller = Seller.objects.first()
        payload = {
            'name': 'José Matias',
            'email': 'josematias@gmail.com',
            'phone': '85986204006'
        }

        response = self.client.put(
            self.base_route + '/' + str(seller.id) + '/', data=payload, follow=True, format="json")

        self.assertTrue(response.data['phone'] == payload['phone'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in response.json())

    def test_delete(self):
        seller = Seller.objects.last()
        response = self.client.delete(
            self.base_route + '/' + str(seller.id) + '/')
        self.assertTrue(status.is_success(response.status_code))
