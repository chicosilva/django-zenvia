# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class Configuracao(models.Model):
    class Meta:
        verbose_name = _(u'Configuração')
        verbose_name_plural = _(u'Configurações')
        ordering = ['nome']

    nome                = models.CharField(verbose_name=_(u'Nome'), max_length=150)
    assinatura_sms      = models.CharField(verbose_name=_(u'Assinatura do SMS'), max_length=150)
    responsavel         = models.CharField(verbose_name=_(u'Responsável'), max_length=150, blank=False, null=False)
    email               = models.EmailField(verbose_name=u'e-mail', max_length=200, help_text=u"Não utilize e-mail de usuários")
    telefone            = models.CharField(verbose_name=_(u'Telefone'), max_length=150, blank=False, null=False)
    celular             = models.CharField(verbose_name=_(u'Celular'), max_length=150, blank=False, null=False,)
    cep                 = models.CharField(verbose_name=_(u'CEP'), max_length=150, blank=False, null=False, help_text=mark_safe('<a class="lbuscacep" target="_blank" href="http://www.buscacep.correios.com.br/servicos/dnec/menuAction.do?Metodo=menuEndereco">Não sabe o CEP? Consulte aqui!</a>'))
    endereco            = models.CharField(verbose_name=_(u'Assinatura do SMS'), max_length=150)
    site                = models.CharField(verbose_name=_(u'Site'), max_length=255, blank=True, null=True)
    aceitou_termos      = models.BooleanField(verbose_name=_(u'Aceitou Termos?'), default=False, blank=True, editable=False)

    def __unicode__(self): return u'%s' % self.nome

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):

        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = _(u'Usuário')
        verbose_name_plural = _(u'Usuários')
        ordering = ['first_name']

    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    celular             = models.CharField(verbose_name=_(u'Celular'), max_length=15, blank=True, null=True,)
    cpf                 = models.CharField(verbose_name=_(u'CPF'), max_length=15, blank=True, null=True,)
    cnpj                = models.CharField(verbose_name=_(u'CNPJ'), max_length=15, blank=True, null=True,)
    cep                 = models.CharField(verbose_name=_(u'CEP'), max_length=150, blank=True, null=True, help_text=mark_safe('<a class="lbuscacep" target="_blank" href="http://www.buscacep.correios.com.br/servicos/dnec/menuAction.do?Metodo=menuEndereco">Não sabe o CEP? Consulte aqui!</a>'))
    endereco            = models.CharField(verbose_name=_(u'Endereço'), max_length=250, blank=True, null=True,)
    numero              = models.CharField(verbose_name=_(u'Número'), max_length=100,  blank=True, null=True,)
    complemento         = models.CharField(verbose_name=_(u'Complemento'), max_length=100, blank=True, null=True,)
    bairro              = models.CharField(verbose_name=_(u'Bairro'), max_length=100, blank=True, null=True,)
    cidade              = models.CharField(verbose_name=_(u'Cidade'), max_length=100, blank=True, null=True,)
    uf                  = models.CharField(verbose_name=_(u'UF'), max_length=100, blank=True, null=True,)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    def __unicode__(self):  return u'%s' % (self.first_name)

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
