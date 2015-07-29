# coding=utf-8
from django.shortcuts import render
from cadastro.models import Usuario, Bairro, Categoria, ORIGEM_CHOICES
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from libs.util import list_paginator
from mensagem.models import Mensagem, MensagemPadrao, StatusMensagem
from conteudo.models import CodigoPromocional, New
from mensagem.api import consulta_status_detalhado
from front.decorators import verifica_termos_uso

@login_required(login_url='/login/')
@verifica_termos_uso()
def index(request):

    # print consulta_status_detalhado('')

    kwargs = {}
    args = []

    categoria       = request.GET.get('categoria', False)
    bairro          = request.GET.get('bairro', False)
    nome            = request.GET.get('nome_celular', False)
    mensagem_padrao = request.GET.get('mensagem_padrao', False)
    status          = request.GET.get('status', False)
    codigo          = request.GET.get('codigo', False)
    noticia         = request.GET.get('noticia', False)
    id_usuario         = request.GET.get('id_usuario', False)

    if categoria: kwargs['categoria'] = categoria
    if codigo: kwargs['codigo_promocional'] = codigo
    if id_usuario: kwargs['usuario'] = id_usuario

    if bairro: kwargs['bairro'] = bairro
    if mensagem_padrao: kwargs['mensagem_padrao'] = mensagem_padrao
    if status: kwargs['status'] = status
    if noticia: kwargs['noticia'] = noticia

    if nome: args = [Q(texto__icontains=nome) | Q(usuario__nome__contains=nome) | Q(usuario__celular__contains=nome)]

    opts_filtros = [200, 999, 5000, 5001, 5002, 000, 10, 13, 100, 110, 111, 120, 133, 134, 150, 160, 161, 171, 190, 01]

    mensagens = Mensagem.objects.filter(*args, **kwargs)

    for mensagem in mensagens:
        mensagem.atualiza_status()

    dados = {
        'titulo': u'SMS - (%s) ' % Mensagem.objects.filter(*args, **kwargs).count(),
        'mensagens': list_paginator(request, mensagens, 20),
        'bairros': Bairro.objects.all(),
        'categorias': Categoria.objects.all(),
        'mensagens_padrao': MensagemPadrao.objects.all(),
        'noticias': New.objects.all(),
        'codigo_promocionais': CodigoPromocional.objects.all(),
        'status': StatusMensagem.objects.filter(codigo__in=opts_filtros),
        'origens': dict(ORIGEM_CHOICES),
        'menu': "menu_mensagens",
    }

    return render(request, 'mensagens/mensagens.html', dados)

@login_required(login_url='/login/')
def msg_padrao(request):
    return render(request, 'mensagens-padrao/mensagens-padrao.html', {'titulo': u'SMS Padrão', 'menu': "menu_mensagem", 'mensagens': list_paginator(request, MensagemPadrao.objects.all(), 50),})

@login_required(login_url='/login/')
def noticias(request):
    return render(request, 'noticias/noticias.html', {'titulo': u'Noticias', 'menu': "menu_conteudo", 'noticias': list_paginator(request, New.objects.all(), 50),})

@login_required(login_url='/login/')
def codigos_promocionais(request):

    kwargs = {}
    args = []

    codigo = request.GET.get('codigo', False)
    if codigo:args = [Q(codigo__icontains=request.GET.get('codigo', False))]

    dados = {
        'titulo': u'Códigos Promocionais',
        'menu': "menu_conteudo",
        'codigos': list_paginator(request, CodigoPromocional.objects.filter(*args, **kwargs), 100),
    }

    return render(request, 'codigos/codigos.html', dados)

@login_required(login_url='/login/')
def clientes(request):

    kwargs = {}
    args = []

    categoria = request.GET.get('categoria', False)
    bairro = request.GET.get('bairro', False)
    nome = request.GET.get('nome_celular', False)
    origem = request.GET.get('origem', False)

    if categoria: kwargs['categoria'] = categoria
    if bairro: kwargs['bairro'] = bairro
    if origem: kwargs['origem'] = origem
    
    if nome: args = [Q(nome__icontains=nome) | Q(celular__contains=nome)]

    dados = {
        'titulo': u'Clientes (%s)' % Usuario.objects.all().count(),
        'clientes': list_paginator(request, Usuario.objects.filter(*args, **kwargs).filter(numero_invalido=False), 50),
        'bairros': Bairro.objects.all(),
        'categorias': Categoria.objects.all(),
        'origens': dict(ORIGEM_CHOICES),
        'menu': "menu_clientes",
    }

    return render(request, 'clientes/clientes.html', dados)

@login_required(login_url='/login/')
def categorias(request):
    return render(request, 'categorias/categorias.html', {'titulo': u'Categorias', 'categorias': Categoria.objects.all(), 'menu': "menu_clientes",})

@login_required(login_url='/login/')
def bairros(request):
    return render(request, 'bairros/bairros.html',{'titulo': u'Bairros', 'bairros': Bairro.objects.all(), 'menu': "menu_clientes",})
