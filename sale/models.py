from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from product.models import Product
from customer.models import Customer
from seller.models import Seller


class Sale(models.Model):
    ''' Classe que representa uma venda '''
    access_key = models.CharField(
        "Nota fiscal", max_length=44, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    seller = models.ForeignKey(
        Seller, on_delete=models.SET_NULL, blank=True, null=True)
    register_datetime = models.DateTimeField(
        "Data de registro", blank=True, null=True)
    total = models.DecimalField(
        "Total", max_digits=16, decimal_places=2, default=0)

    def __str__(self):
        return '# {}'.format(str(self.id))

    def save(self, *args, **kwargs):
        if not self.register_datetime:
            self.register_datetime = timezone.now()
        return super(Sale, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'venda'
        verbose_name_plural = 'vendas'

    def set_total(self):
        total = 0
        for item in self.saleproduct_set.all():
            total += item.total
        self.total = total


class SaleProduct(models.Model):
    ''' Classe que representa o produto de uma venda '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=False)
    quantity = models.PositiveIntegerField(
        "Quantidade", blank=False, null=False)
    _commission_applied = models.DecimalField(
        "Comissão aplicada", max_digits=3, decimal_places=1, default=0)
    total = models.DecimalField(
        "Total", max_digits=16, decimal_places=2, default=0)

    def __str__(self):
        return "{} x {}".format(self.product.description, self.quantity)

    def save(self, *args, **kwargs):
        self.set_total()
        self.set_commission_applied()

        return super(SaleProduct, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'produto da venda'
        verbose_name_plural = 'produtos da venda'

    @property
    def commission_applied(self):
        return self._commission_applied

    @commission_applied.setter
    def commission_applied(self, value):
        self._commission_applied = value

    def set_commission_applied(self):
        day_week = self.sale.register_datetime.weekday() + 1
        percentage = self.product.commission_percentage

        try:
            commission_schedule = self.product.productcommissionschedule_set.get(
                day_week=day_week)
        except ObjectDoesNotExist:
            commission_schedule = None
            self.commission_applied = percentage

        if commission_schedule:
            if percentage >= commission_schedule.min_percentage and percentage <= commission_schedule.max_percentage:
                self.commission_applied = percentage
            if percentage < commission_schedule.min_percentage:
                self.commission_applied = commission_schedule.min_percentage
            if percentage > commission_schedule.max_percentage:
                self.commission_applied = commission_schedule.max_percentage

    def set_total(self):
        self.total = self.product.unit_price * self.quantity


@receiver(post_save, sender=SaleProduct)
def set_update_total_sale(sender, created, instance=None, **kwargs):
    instance.sale.set_total()
    instance.sale.save()
