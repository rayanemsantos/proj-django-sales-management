import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response

from sale.models import Sale
from seller.models import Seller
from sale.serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-register_datetime')
    serializer_class = SaleSerializer


class SaleCommissionsViewSet(viewsets.GenericViewSet):
    queryset = ''

    def list(self, request):
        date_init = request.GET.get('date_init', None)
        date_end = request.GET.get('date_end', None)

        if date_init and date_end:
            try:
                try:
                    date_init = datetime.datetime.strptime(
                        date_init, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
                    date_end = datetime.datetime.strptime(
                        date_end, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
                except Exception as e:
                    raise ValueError(str(e))

                sales = Sale.objects.filter(
                    register_datetime__gte=date_init, register_datetime__lte=date_end)

                sellers = Seller.objects.all()

                commissions = list()
                total = 0

                for seller in sellers:
                    seller_sales = sales.filter(seller=seller)

                    if seller_sales.exists():
                        seller_total_commission = 0

                        for _item in seller_sales:
                            seller_total_commission += _item.total_commission

                        _commission = {
                            'seller': seller.name,
                            'total_sales': seller_sales.count(),
                            'total_commission': seller_total_commission
                        }
                        commissions.append(_commission)
                        total += _commission['total_commission']

                serializer_data = {
                    'results': commissions,
                    'total': total
                }

                return Response(serializer_data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
