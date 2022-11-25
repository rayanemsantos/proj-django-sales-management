from rest_framework import viewsets, status
from rest_framework.response import Response
from sale.models import Sale
from sale.serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
