from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import routers
from seller import urls as seller_routes

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

routeLists = [
    seller_routes.routeList
]

for routeList in routeLists:
    for route in routeList:
        router.register(route[0], route[1])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
