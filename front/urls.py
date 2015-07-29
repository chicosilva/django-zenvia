# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('front.views',
                       url(r'^$', 'index', name='index'),
                       url(r'^clientes/$', 'clientes', name='clientes'),
                       url(r'^categorias/$', 'categorias', name='categorias'),
                       url(r'^bairros/$', 'bairros', name='bairros'),
                       url(r'^codigos-promocionais/$', 'codigos_promocionais', name='codigos_promocionais'),
                       url(r'^noticias/$', 'noticias', name='noticias'),
                       url(r'^msg-padrao/$', 'msg_padrao', name='msg_padrao'),

)