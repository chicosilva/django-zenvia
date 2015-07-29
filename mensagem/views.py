# coding=utf-8
from django.contrib.auth.decorators import login_required
import datetime
import json
from mensagem.forms import MensagemUsuarioEspecificoForm, MensagemUsuarioSelecaoForm, MensagemCodigoPromocinalForm, NoticiaForm, DetalheMensagemForm, MensagemPadraoForm
from mensagem.models import Mensagem, MensagemPadrao, data_agendamento, CodigoPromocional, save_envio_mensagem_conteudo, reenviar_mensagem, FilaMensagem
from django.contrib import messages
from django.core.urlresolvers import reverse
from cadastro.models import Usuario
from conteudo.models import New
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from mensagem.api import cancelar_agendamento_api, enviar_sms_api, consulta_sms_marketing_recebidos, enviar_sms_teste, consulta_status_detalhado

@login_required(login_url='/login/')
def nova_mensagem_selecao(request):

    if request.method == 'POST':

        form = MensagemUsuarioSelecaoForm(request.POST)

        if form.is_valid():

            dados_form = {
                'data_agendamento': data_agendamento(request.POST.get('data_agendamento', False), request.POST.get('hora_envio', False)),
                'mensagem_padrao_id': request.POST.get('mensagem_padrao', False),
                'enviar_link': request.POST.get('enviar_link', False),
                'texto': request.POST.get('texto'),
                'status_id': 40,
                'tipo_id': request.POST.get('tipo'),
            }

            kwargs = {}

            categoria = request.POST.get('categoria', False)
            bairro = request.POST.get('bairro', False)

            if categoria:
                kwargs['categoria'] = categoria
                dados_form['categoria_id'] = categoria

            if bairro:
                kwargs['bairro'] = bairro
                dados_form['bairro_id'] = bairro

            if dados_form['tipo_id'] == '2':
                usuarios = Usuario.objects.filter(**kwargs).filter(numero_invalido=False).filter(notificacoes=True)
            else:
                usuarios = Usuario.objects.filter(**kwargs).filter(numero_invalido=False)

            for usuario in usuarios:

                dados_form['usuario'] = usuario
                Mensagem(**dados_form).save()

            messages.success(request, u"SMS enviado com sucesso, confira o status")
            return redirect(reverse('front:index'))

    else:
        form = MensagemUsuarioSelecaoForm()

    dados = {
        'form': form,
        'mensagens_padrao': MensagemPadrao.objects.all(),
        'usuarios': Usuario.objects.filter(numero_invalido=False),
        'titulo': u'SMS para usuários específicos',
        'menu': "menu_mensagens",

    }

    return render(request, 'mensagens/novo_selecao.html', dados)

@login_required(login_url='/login/')
def nova_mensagem(request):

    if request.method == 'POST':

        form = MensagemUsuarioEspecificoForm(request.POST)

        if form.is_valid():

            l = []

            for usuario in request.POST.getlist('usuarios'): l.append(usuario)

            dados_form = {
                'data_agendamento': data_agendamento(request.POST.get('data_agendamento', False), request.POST.get('hora_envio', False)),
                'mensagem_padrao_id': request.POST.get('mensagem_padrao', False),
                'texto': request.POST.get('texto'),
                'particular': 1,
                'status_id': 40,
                'enviar_link': request.POST.get('enviar_link', False),
                'tipo_id': request.POST.get('tipo'),
            }

            if dados_form['tipo_id'] == '2':
                usuarios = Usuario.objects.filter(pk__in=l).filter(notificacoes=True)
            else:
                usuarios = Usuario.objects.filter(pk__in=l)

            for usuario in usuarios:
                dados_form['usuario'] = usuario
                Mensagem(**dados_form).save()

            messages.success(request, u"SMS enviado com sucesso, confira o status")

            return redirect(reverse('front:index'))

    else:
        form = MensagemUsuarioEspecificoForm()

    dados = {'form': form,
             'mensagens_padrao': MensagemPadrao.objects.all(),
             'usuarios': Usuario.objects.filter(numero_invalido=False),
             'titulo': u'SMS para usuários específicos',
             'menu': "menu_mensagens",
             }

    return render(request, 'mensagens/novo.html', dados)

@login_required(login_url='/login/')
def nova_mensagem_codigo_promocional(request):

    if request.method == 'POST':

        form = MensagemCodigoPromocinalForm(request.POST)

        if form.is_valid():

            save_envio_mensagem_conteudo(request, 'codigo_promocional')
            messages.success(request, u"SMS enviado com sucesso, confira o status")
            return redirect(reverse('front:index'))

    else:
        form = MensagemCodigoPromocinalForm()

    dados = {'form': form,
             'codigos_promocionais': CodigoPromocional.objects.all(),
             'titulo': u'Enviar Código Promocional',
             'menu': "menu_mensagens",
            }
    return render(request, 'mensagens/novo_codigo_promocional.html', dados)

@login_required(login_url='/login/')
def nova_mensagem_noticia(request):

    if request.method == 'POST':

        form = NoticiaForm(request.POST)

        if form.is_valid():

            save_envio_mensagem_conteudo(request, 'noticia')
            messages.success(request, "Mensagem enviada com sucesso, confira o status")
            return redirect(reverse('front:index'))

    else:
        form = NoticiaForm()

    return render(request, 'mensagens/novo_noticia.html', {'form': form, 'noticias': New.objects.all(),'titulo': u'Enviar SMS com Link de Notícia', 'menu': "menu_mensagens",})

@login_required(login_url='/login/')
def cancelar_agendamento(request, id):

    mensagem = get_object_or_404(Mensagem, pk=id)
    tela_usuario = request.GET.get('tela_usuario', '0')

    if request.method == 'POST':
        tela_usuario = request.POST.get('tela_usuario')
        cancelar_agendamento_api(mensagem)
        messages.success(request, 'Agendamento cancelado com sucesso!')

        if tela_usuario == "0": return redirect(reverse('front:index'))

        return redirect(reverse('cadastro:detalhes', kwargs={'id':mensagem.usuario.pk}))

    return render(request, 'mensagens/cancelar.html', {'mensagem': mensagem, 'titulo': u'Cancelar Agendamento', 'tela_usuario': tela_usuario, 'menu': "menu_mensagens",})

@login_required(login_url='/login/')
def massa(request):

    if request.method == 'POST':
        mensagens = request.POST.getlist('mensagem')
        acao = request.POST.get('acao')

        if acao == '0':
            messages.success(request, u'Escolha uma ação!')
            return redirect(reverse('front:index'))

        for id in mensagens:

            mensagem = get_object_or_404(Mensagem, pk=id)

            if acao == 'cancelar_agendamento': cancelar_agendamento_api(mensagem)

            if acao == 'novo_envio':
                reenviar_mensagem(id)

        if acao == 'cancelar_agendamento':
            messages.success(request, 'Agendamento cancelado com sucesso!')

        if acao == 'novo_envio':
            messages.success(request, 'Envios efetuados com sucesso, confira o status.')

        return redirect(reverse('front:index'))

def detalhe_mensagem(request):

    if not request.user_agent.is_mobile: return HttpResponse(json.dumps({}), content_type="application/json")

    id = request.GET.get('i', False)

    mensagem = Mensagem.objects.get(pk=id)

    if request.method == 'POST':

        form = DetalheMensagemForm(request.POST)

        if form.is_valid():

            messages.success(request, 'Resposta enviada com sucesso! Obrigado.')
            mensagem.resposta = request.POST.get('resposta')
            mensagem.save()
    else:
        form = DetalheMensagemForm()

    from autenticacao.models import Configuracao
    configuracao = Configuracao.objects.all().first()

    dados = {
            'titulo': configuracao.nome,
            'mensagem': mensagem,
            'form': form,
            'menu': "menu_conteudo",
    }

    mensagem.clicada = True
    mensagem.save()

    return render(request, 'mensagens/detalhes.html', dados)

def fila(request):

    mensagens = FilaMensagem.objects.all()[:15]

    if mensagens:

        for item in mensagens:

            try:
                enviar_sms_api(item.mensagem)
            except:
                pass

            item.data_cancelamento = datetime.datetime.now()
            item.save()

    return HttpResponse(json.dumps({}), content_type="application/json")

def mensagens_recebidas(request):

    r = consulta_sms_marketing_recebidos()
    return HttpResponse(json.dumps(r), content_type="application/json")

@login_required(login_url='/login/')
def exemplos(request):
    return render(request, 'mensagens/exemplos.html', {'titulo': u'Exemplos de SMS', 'menu': "menu_mensagens",})

@login_required(login_url='/login/')
def diferenca(request):
    return render(request, 'mensagens/diferenca.html', {'titulo': u'Diferença entre SMS Corporativo e Marketing', 'menu': "menu_mensagens",})

@login_required(login_url='/login/')
def link_confirmacao(request):
    return render(request, 'mensagens/link_confirmacao.html', {'titulo': u'Link de Confirmação', 'menu': "menu_mensagens",})

@login_required(login_url='/login/')
def faq(request):
    return render(request, 'mensagens/faq.html', {'titulo': u'Perguntas Frequentes','menu': "menu_faq",})

@login_required(login_url='/login/')
def mensagem_teste(request):

    texto = request.GET.get('texto', False)
    form_marketing = request.GET.get('form_marketing')

    if not texto:
        return HttpResponse(json.dumps({'sucesso': False, 'form_marketing': form_marketing, 'texto': False }), content_type="application/json")

    try:

        enviar_sms_teste(texto)
        return HttpResponse(json.dumps({'sucesso': True}), content_type="application/json")
    except:
        pass

    return HttpResponse(json.dumps({'sucesso': False}), content_type="application/json")

@login_required(login_url='/login/')
def nova_msg_padrao(request):

    if request.method == 'POST':

        form = MensagemPadraoForm(request.POST)

        if form.is_valid():

            form.save()
            messages.success(request, u"SMS cadastrado com sucesso!")
            return redirect(reverse('front:msg_padrao'))

    else:
        form = MensagemPadraoForm()

    dados = {
        'form': form,
        'menu': "menu_mensagem",
        'titulo': u'Cadastrar SMS Padrão',
    }

    return render(request, 'mensagens-padrao/novo.html', dados)

@login_required(login_url='/login/')
def editar_msg_padrao(request, id):

    mensagem = MensagemPadrao.objects.get(pk=id)

    if request.method == 'POST':
        form = MensagemPadraoForm(request.POST, instance=mensagem)
        if form.is_valid():
            messages.success(request, u'SMS atualizado com sucesso!')
            form.save()

            return redirect(reverse('front:msg_padrao'))
    else:
        form = MensagemPadraoForm(instance=mensagem)

    dados = {
            'titulo': u'Editar SMS Padrão',
            'form': form,
            'menu': "menu_mensagem",
            'mensagem': mensagem
    }

    return render(request, 'mensagens-padrao/novo.html', dados)
