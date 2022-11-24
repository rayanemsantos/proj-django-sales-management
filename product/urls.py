from .views import ProductViewSet

app_name = "product"

routeList = (
    (r'product', ProductViewSet),
)
