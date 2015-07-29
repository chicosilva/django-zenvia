# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('autenticacao.views',

                       url(r'^sair/$', 'sair', name='sair'),
                       url(r'^login/$', 'entrar', name='login'),
                       url(r'^configuracoes/$', 'configuracoes', name='configuracoes'),
                       url(r'^termos-de-uso/$', 'termos', name='termos'),
                       url(r'^editar-senha/$', 'editar_senha', name='editar_senha'),
                       url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'restaurar_senha', name='password_reset_confirm'),
                       url(r'^reset/$', 'reset', name='reset'),

)