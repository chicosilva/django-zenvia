# coding=utf-8
from django.conf.urls import patterns, url
urlpatterns = patterns('mensagem.views',

        url(r'^enviar-mensagem/$', 'nova_mensagem', name='nova_mensagem'),
        url(r'^enviar-mensagem-selecao/$', 'nova_mensagem_selecao', name='nova_mensagem_selecao'),
        url(r'^enviar-codigo-promocional/$', 'nova_mensagem_codigo_promocional', name='nova_mensagem_codigo_promocional'),
        url(r'^enviar-noticia/$', 'nova_mensagem_noticia', name='nova_mensagem_noticia'),
        url(r'^cancelar-agendamento/(?P<id>\d+)$', 'cancelar_agendamento', name='cancelar_agendamento'),
        url(r'^massa/$', 'massa', name='massa'),
        url(r'^fila/$', 'fila', name='fila'),
        url(r'^d/$', 'detalhe_mensagem', name='detalhe_mensagem'),
        url(r'^exemplos/$', 'exemplos', name='exemplos'),
        url(r'^diferenca/$', 'diferenca', name='diferenca'),
        url(r'^link-confirmacao/$', 'link_confirmacao', name='link_confirmacao'),
        url(r'^faq/$', 'faq', name='faq'),
        url(r'^recebidas/$', 'mensagens_recebidas', name='mensagens_recebidas'),
        url(r'^mensagem-teste/$', 'mensagem_teste', name='mensagem_teste'),
        url(r'^nova-msg-padrao/$', 'nova_msg_padrao', name='nova_msg_padrao'),
        url(r'^editar-msg-padrao/(?P<id>\d+)$', 'editar_msg_padrao', name='editar_msg_padrao'),
)