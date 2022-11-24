from .views import CustomerViewSet

app_name = "customer"

routeList = (
    (r'customer', CustomerViewSet),
)
