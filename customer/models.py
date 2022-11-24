from common.models import Person


class Customer(Person):
    ''' Implementa Person para Customer '''

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(Customer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
