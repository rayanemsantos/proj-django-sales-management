from django.db import models


class Person(models.Model):
    ''' Classe base de pessoa '''
    name = models.CharField("Nome", max_length=255, null=True, blank=True)
    email = models.CharField("E-mail", max_length=255, null=True, blank=True)
    phone = models.CharField("Telefone", max_length=13, null=True, blank=True)

    class Meta:
        abstract = True
