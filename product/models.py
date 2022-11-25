from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .constants import DAY_WEEK_CHOICES


def validate_commission_percentage(value):
    if value > 10:
        raise ValidationError(
            _('%(value)s Porcentagem máxima permitida = 10'),
            params={'value': value},
        )


class Product(models.Model):
    ''' Classe que representa um produto '''
    code = models.IntegerField("Código", db_index=True, unique=True)
    description = models.TextField("Descrição", null=True, blank=True)
    unit_price = models.DecimalField(
        "Preço unitário", max_digits=16, decimal_places=2, blank=True, null=True)
    commission_percentage = models.DecimalField(
        "Porcentagem de comissão", max_digits=3, decimal_places=1, default=0, validators=[validate_commission_percentage])

    def __str__(self):
        return "{} - {}".format(self.code, self.description)

    def save(self, *args, **kwargs):
        return super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'


class ProductCommissionSchedule(models.Model):
    ''' Classe que representa a agenda de comissão de um produto '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    day_week = models.PositiveIntegerField(
        "Dia da semana", choices=DAY_WEEK_CHOICES, null=False)
    min_percentage = models.DecimalField(
        "Porcentagem mínima", max_digits=3, decimal_places=1, blank=True, null=True, validators=[validate_commission_percentage])
    max_percentage = models.DecimalField(
        "Porcentagem máxima", max_digits=3, decimal_places=1, blank=True, null=True, validators=[validate_commission_percentage])

    def __str__(self):
        return "{} - {}".format(self.get_day_week_display(), self.product.description)

    def save(self, *args, **kwargs):
        return super(ProductCommissionSchedule, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'agenda de comissão do produto'
        verbose_name_plural = 'agendas de comissão dos produtos'
        unique_together = ('day_week', 'product',)

    def get_day_week_display(self):
        for code, label in DAY_WEEK_CHOICES:
            if self.day_week == code:
                break
        return label
