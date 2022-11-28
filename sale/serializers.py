from rest_framework import serializers
from rest_framework.serializers import as_serializer_error
from sale.models import Sale, SaleProduct
from product.serializers import ProductSerializer


class SaleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleProduct
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = '' if instance.product == "" or instance.product == None else ProductSerializer(
            instance.product).data
        response['total_commission'] = '' if instance.total_commission == "" or instance.total_commission == None else instance.total_commission
        return response


class SaleSerializer(serializers.ModelSerializer):
    sale_products = SaleProductSerializer(
        source="saleproduct_set", many=True, read_only=True)

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
            except Exception as e:
                raise ValueError(str(e))
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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = '' if instance.customer == "" or instance.customer == None else {
            "id": instance.customer.id, "name": instance.customer.name}
        response['seller'] = '' if instance.seller == "" or instance.seller == None else {
            "id": instance.seller.id, "name": instance.seller.name}
        response['total_commission'] = '' if instance.total_commission == "" or instance.total_commission == None else instance.total_commission
        return response
