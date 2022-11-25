from django.urls import path
from .views import SaleViewSet, SaleCommissionsViewSet

app_name = "sale"

routeList = (
    (r'sale', SaleViewSet),
    (r'sale_commissions', SaleCommissionsViewSet, 'sale_commissions'),
)
