import re
from django.db import models


class Person(models.Model):
    ''' Classe base de pessoa '''
    name = models.CharField("Nome", max_length=255, null=True, blank=True)
    email = models.CharField("E-mail", max_length=255, null=True, blank=True)
    phone = models.CharField("Telefone", max_length=13, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.format_phone()
        return super(Person, self).save(*args, **kwargs)

    def format_phone(self):
        '''
        Retorna phone sem formatação (somente números)
        :return: phone
        '''
        if self.phone:
            self.phone = re.sub('[()/-/+]', '', self.phone)
            self.phone = self.phone.replace(" ", "")
            self.phone = self.phone[-11:]
