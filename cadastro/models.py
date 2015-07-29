# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
import re

class Usuario(models.Model):
    class Meta:
        verbose_name = _(u'Cliente')
        verbose_name_plural = _(u'Clientes')
        ordering = ['nome']

    nome                = models.CharField(verbose_name=_(u'Nome'), max_length=150, blank=True, null=True,)
    data_nascimento     = models.DateField(verbose_name=_(u'Data de Nascimento'), auto_now_add=False, blank=True, null=True)
    celular             = models.CharField(verbose_name=_(u'Celular'), max_length=15, unique=True)
    numero_invalido     = models.BooleanField(verbose_name=_(u'Número Inválido?'), default=False, blank=True, )

    def __unicode__(self):
        if not self.nome: return u"Cliente 00%s" % self.pk
        return u'%s' % (self.nome)

    def celular_tostr(self):

        if len(self.celular) >= 11: return '(%s) %s - %s' %(self.celular[0:2], self.celular[2:7], self.celular[7:11])
        return '(%s) %s - %s' %(self.celular[0:2], self.celular[2:6], self.celular[6:11])

def celular_to_int(numero):

    celular = re.sub('[()-]', '', numero)
    celular = celular.replace(" ", "")

    if int(celular[:1]) == 0:
        celular = celular[1:]

    if len(celular) < 9:
        return False

    if len(celular) > 11:
        return False

    ddds = range(11,99)
    ddd = int(celular[:2])

    if not ddd in ddds:
        return False

    return celular