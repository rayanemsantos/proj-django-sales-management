from .views import SellerViewSet

app_name = "selelr"

routeList = (
    (r'seller', SellerViewSet),
)
