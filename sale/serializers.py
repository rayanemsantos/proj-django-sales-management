from rest_framework import serializers
from rest_framework.serializers import as_serializer_error
from sale.models import Sale


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ('total',)

    def is_valid(self, raise_exception=False):
        return super(SaleSerializer, self).is_valid(raise_exception=raise_exception)

    def validate(self, data):
        try:
            context = self.context["request"].data
            try:
                products = context['products']
            except Exception:
                raise ValueError("field 'products' required")

            if not isinstance(products, list):
                raise ValueError("field 'products' should be a list")

        except Exception as e:
            print(e)
            raise serializers.ValidationError(e)

        return data

    def create(self, validated_data):
        context = self.context["request"].data
        products = context['products']

        sale = super(SaleSerializer, self).create(validated_data)

        for _product in products:
            try:
                sale.saleproduct_set.create(
                    product_id=_product['product'],
                    quantity=int(_product['quantity'])
                )
            except Exception:
                pass
        return sale

    def update(self, sale, validated_data):
        context = self.context["request"].data
        products = context['products']

        sale = super(SaleSerializer, self).update(sale, validated_data)

        products_list_id = list()

        for _product in products:
            id = None if not 'id' in _product else _product['id']
            try:
                saleproduct, _ = sale.saleproduct_set.get_or_create(
                    id=id,
                    defaults={
                        'product_id': _product['product'],
                        'quantity': int(_product['quantity'])
                    }
                )
                products_list_id.append(saleproduct.id)
            except Exception:
                pass

        sale.saleproduct_set.exclude(id__in=products_list_id).delete()

        return sale
