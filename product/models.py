from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
