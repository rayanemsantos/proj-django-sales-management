from common.models import Person


class Seller(Person):
    ''' Implementa Person para Seller '''

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(Seller, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'vendedor'
        verbose_name_plural = 'vendedores'
