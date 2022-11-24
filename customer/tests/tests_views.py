import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from customer.tests.tests_models import SetupData as CustomerSetup
from customer.models import Customer


class CustomerViewSetTestCase(TestCase):

    def setUp(self):
        self.start = CustomerSetup()
        self.client = APIClient()
        self.start.create_customer()
        self.base_route = '/api/customer'

    def test_list(self):
        response = self.client.get(self.base_route, follow=True)
        content = json.loads(response.content.decode("utf-8"))
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in content[0])

    def test_get_object(self):
        customer = Customer.objects.first()
        response = self.client.get(
            self.base_route + '/' + str(customer.id), follow=True)
        content = json.loads(response.content.decode("utf-8"))
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in content)

    def test_post(self):
        payload = {
            'name': 'Rayane Maria',
            'email': 'rayanemsantos.contato@gmail.com',
            'phone': '85987234658'
        }
        response = self.client.post(
            self.base_route + '/', data=payload, follow=True, format="json")

        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in response.json())

    def test_put(self):
        customer = Customer.objects.first()
        payload = {
            'name': 'Rayane Maria',
            'email': 'rayanemsantos.contato@gmail.com',
            'phone': '8598786547'
        }

        response = self.client.put(
            self.base_route + '/' + str(customer.id) + '/', data=payload, follow=True, format="json")

        self.assertTrue(response.data['phone'] == payload['phone'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue("id" in response.json())

    def test_delete(self):
        customer = Customer.objects.last()
        response = self.client.delete(
            self.base_route + '/' + str(customer.id) + '/')
        self.assertTrue(status.is_success(response.status_code))
