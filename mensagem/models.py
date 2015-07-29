# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from cadastro.models import Usuario
import datetime

class StatusMensagem(models.Model):
    class Meta:
        verbose_name = _(u'Mensagem')
        verbose_name_plural = _(u'Mensagens')
        ordering = ['-pk']

    codigo              = models.CharField(verbose_name=_(u'Status'), max_length=25, editable=False)
    descricao           = models.CharField(verbose_name=_(u'Descrição'), max_length=250, editable=False)
    consultar_api       = models.BooleanField(verbose_name=_(u'Permitir consulta na APi?'), default=False, blank=True, )
    tarifar             = models.BooleanField(verbose_name=_(u'Tarifar?'), default=False, blank=True, )

    def __unicode__(self): return u'%s' % self.descricao

    def style(self):
        codigos = {'120': 'success', '999': 'danger', '015': 'danger'}
        try:
            return codigos[self.codigo]
        except:
            return "label"

class Mensagem(models.Model):
    class Meta:
        verbose_name = _(u'Mensagem')
        verbose_name_plural = _(u'Mensagens')
        ordering = ['-id']

    status              = models.ForeignKey(StatusMensagem, verbose_name=_(u'Status Mensagem'), editable=False, default=42)
    usuario             = models.ForeignKey(Usuario, verbose_name=_(u'Usuário'), editable=False)
    texto               = models.TextField(verbose_name=_(u'Texto'), max_length=149,)
    destino             = models.CharField(verbose_name=_(u'Destino'), max_length=30, blank=True, null=False)
    data_agendamento    = models.DateTimeField(verbose_name=_(u'Data de Agendamento'), blank=True, null=True)
    data                = models.DateField(verbose_name=_(u'Data de envio'), auto_now_add=True)
    status_text         = models.TextField(verbose_name=_(u'Texto Status'), max_length=150, blank=True, null=True)

    def __unicode__(self): return u'%s' % self.campanha

    def atualiza_status(self):

        from mensagem.api import consulta_sms
        consulta_sms(self)
        return ''

    def save(self, *args, **kwargs):
        self.destino = self.usuario.celular
        super(Mensagem, self).save(*args, **kwargs)

    def celular_tostr(self):

        if len(self.destino) >= 11: return '(%s) %s - %s' %(self.destino[0:2], self.destino[2:7], self.destino[7:11])
        return '(%s) %s - %s' %(self.destino[0:2], self.destino[2:6], self.destino[6:11])

    def celular_tostr(self):

        if len(self.destino) >= 11: return '(%s) %s - %s' %(self.destino[0:2], self.destino[2:7], self.destino[7:11])
        return '(%s) %s - %s' %(self.destino[0:2], self.destino[2:6], self.destino[6:11])

def data_agendamento(data_agendamento, hora_envio):

    if not data_agendamento:
        return None

    hora = "09:00"

    if data_agendamento:
        if hora_envio: hora = hora_envio
        data_agendamento = datetime.datetime.strptime("%s %s:00" % (data_agendamento, hora), '%d/%m/%Y %H:%M:%S')

    return data_agendamento