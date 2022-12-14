
from faker import Faker

import django
import os
import sys
import json
import random
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'sales_management.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sales_management.settings")
django.setup()

from customer.models import Customer
from seller.models import Seller
from product.models import Product

fake = Faker('pt_BR')


def generate_customer():
    for index in range(20):
        Customer.objects.create(
            name=fake.name(),
            email=fake.email(),
            phone=fake.cellphone_number()
        )


def generate_seller():
    for index in range(20):
        Seller.objects.create(
            name=fake.name(),
            email=fake.email(),
            phone=fake.cellphone_number()
        )


def generate_products():
    data = []

    with open('scripts/products.json') as fp:
        data = json.load(fp)

    for item in data:
        try:
            Product.objects.get_or_create(
                code=item['id'],
                description=item['title'],
                unit_price=item['price'],
                commission_percentage=random.randint(1, 9),
            )
        except:
            pass


def db_seed():
    # generate_customer()
    # generate_seller()
    generate_products()


if __name__ == "__main__":
    print("Iniciado o script...")
    db_seed()
    print("Pronto! :)")
