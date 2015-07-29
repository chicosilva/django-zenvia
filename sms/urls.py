# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

                       url(r'^gestao/', include(admin.site.urls)),
                       url('', include('cadastro.urls', namespace='cadastro')),
                       url('', include('localizacao.urls', namespace='localizacao')),
                       url('', include('front.urls', namespace='front')),
                       url('', include('mensagem.urls', namespace='mensagem')),
                       url('', include('conteudo.urls', namespace='conteudo')),
                       url('', include('financeiro.urls', namespace='financeiro')),
                       url('', include('autenticacao.urls', namespace='autenticacao')),
                       url(r'^retorno/pagseguro/', include('pagseguro.urls')),

)

if settings.DEBUG:
    urlpatterns = patterns('',
                           url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                           url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    ) + urlpatterns