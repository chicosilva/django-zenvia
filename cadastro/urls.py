# coding=utf-8
from django.conf.urls import patterns, url
urlpatterns = patterns('cadastro.views',
        url(r'^detalhe-cliente/(?P<id>\d+)$', 'detalhes', name='detalhes'),
        url(r'^desabilitar-recebimento-campanha/(?P<id>\d+)$', 'desabilitar_recebimento_campanha', name='desabilitar_recebimento_campanha'),
        url(r'^editar-cliente/(?P<id>\d+)$', 'editar', name='editar'),
        url(r'^novo-cliente/$', 'novo', name='novo'),
        url(r'^importar-planilha/$', 'importar_planilha', name='importar_planilha'),
        url(r'^editar-categoria/(?P<id>\d+)$', 'editar_categoria', name='editar_categoria'),
        url(r'^novo-categoria/$', 'nova_categoria', name='nova_categoria'),
        url(r'^cancelar-categoria/(?P<id>\d+)$', 'cancelar_categoria', name='cancelar_categoria'),
        url(r'^numeros-invalidos/$', 'numeros_invalidos', name='numeros_invalidos'),
        url(r'^remover-numeros-invalidos/$', 'remover_numeros_invalidos', name='remover_numeros_invalidos'),
)