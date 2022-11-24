from django.test import TestCase
from seller.models import Seller


class SetupData:
    def create_seller(self):
        self.customer = Seller.objects.create(
            name='José Matias',
            email='josematias@gmail.com',
            phone='85986203456'
        )


class CustomerTestCase(TestCase):
    start = SetupData()

    def setUp(self):
        self.start.create_seller()

    def test_get(self):
        seller = Seller.objects.first()
        self.assertIsInstance(seller, Seller)

    def test_update(self):
        seller = Seller.objects.first()
        seller.name = 'José Matias'
        seller.save()
        self.assertEqual(seller.name, 'José Matias')

    def test_str(self):
        seller = Seller.objects.first()
        self.assertEqual(seller.__str__(), 'José Matias')

    def test_delete(self):
        seller = Seller.objects.first()
        seller.delete()

        self.assertFalse(seller.id)
        self.assertIsInstance(seller, Seller)
