from .views import SellerViewSet

app_name = "seller"

routeList = (
    (r'seller', SellerViewSet),
)
