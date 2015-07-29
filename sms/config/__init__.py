# coding=utf-8
from os.path import join, dirname
from django.conf import settings

TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS
STATICFILES_FINDERS = settings.STATICFILES_FINDERS
INSTALLED_APPS = settings.INSTALLED_APPS
STATIC_URL = settings.STATIC_URL
import socket

DOMINIO = 'http://localhost:8000'
NOME_SITE = u'Local Host'

if socket.gethostname() == 'meuhost':
    from local_settings import *
else:
    if socket.gethostname() != 'meuhost':
        from production_settings import *

RAIZ = dirname(dirname(__file__))
PUBLIC_ROOT = join(RAIZ, 'public')
MEDIA_ROOT = join(PUBLIC_ROOT, 'media')
STATIC_ROOT = join(PUBLIC_ROOT, 'static')
LOG_ROOT = join(PUBLIC_ROOT, 'logs')
TEMPLATE_DIRS = (join(RAIZ, 'templates'), )
STATIC_URL = '/static/'
MEDIA_URL = '/media/'


INSTALLED_APPS = ('suit',) + INSTALLED_APPS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    "financeiro.processor.informacoes_financeiras",
)

STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)
from apps import INSTALLED_APPS as IA

INSTALLED_APPS += IA

