from .views import SaleViewSet

app_name = "sale"

routeList = (
    (r'sale', SaleViewSet),
)
