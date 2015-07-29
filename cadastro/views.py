# coding=utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from cadastro.forms import UsuarioForm, CategoriaForm, ImportPlanilhaForm, RemoverNumeroForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from libs.util import handle_uploaded_file
import datetime
from keepsms.config import MEDIA_ROOT
from cadastro.models import Usuario, importa_arquivo_csv, Categoria, celular_to_int
from mensagem.models import Mensagem, MensagemPadrao, data_agendamento
from mensagem.forms import MensagemParticularForm
from libs.util import list_paginator

@login_required(login_url='/login/')
def novo(request):

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Cliente adicionando com sucesso!')
            usuario = form.save()

            if request.POST['salvar'] == '1':
                return redirect(reverse('cadastro:detalhes', kwargs={'id':usuario.pk}))

            return redirect(reverse('cadastro:novo'))
    else:
        form = UsuarioForm()

    return render(request, 'clientes/novo.html', {'titulo': u'Cadastrar Novo Cliente', 'form': form, 'menu': "menu_clientes",})

@login_required(login_url='/login/')
def editar(request, id):

    usuario = get_object_or_404(Usuario, pk=id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            messages.success(request, 'Cliente atualizado com sucesso!')
            form.save()
            return redirect(reverse('cadastro:detalhes', kwargs={'id':usuario.pk}))
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'clientes/editar.html', {'titulo': u'Editar Cliente', 'form': form, 'usuario': usuario, 'menu': "menu_clientes",})

@login_required(login_url='/login/')
def numeros_invalidos(request):

    numeros_invalidos = Usuario.objects.filter(numero_invalido=True)
    return render(request, 'clientes/invalidos.html', {'titulo': u'Números Inválidos (%s)' % numeros_invalidos.count(),
                                                       'clientes': list_paginator(request, numeros_invalidos, 100),
                                                       'menu': "menu_clientes",
                                                       })

@login_required(login_url='/login/')
def remover_numeros_invalidos(request):

    if request.method == 'POST':
            Usuario.objects.filter(numero_invalido=True).delete()
            messages.success(request, u'Números removidos com sucesso!')

    return redirect(reverse('cadastro:numeros_invalidos'))

@login_required
def desabilitar_recebimento_campanha(request, id):

    if request.method == 'POST':
            Usuario.objects.filter(id=id).update(notificacoes=False)
            messages.error(request, u'O Cliente não receberá campanhas', extra_tags='danger')

    return redirect(reverse('cadastro:detalhes', kwargs={'id':id}))

@login_required(login_url='/login/')
def detalhes(request, id):

    usuario = get_object_or_404(Usuario, pk=id)

    if request.method == 'POST':

            form = MensagemParticularForm(request.POST)

            if form.is_valid():
                dados_form = {
                    'data_agendamento': data_agendamento(request.POST.get('data_agendamento', False), request.POST.get('hora_envio', False)),
                    'mensagem_padrao_id': request.POST.get('mensagem_padrao', False),
                    'texto': request.POST.get('texto'),
                    'enviar_link': request.POST.get('enviar_link', False),
                    'usuario': usuario,
                    'particular': 1,
                    'tipo_id': request.POST.get('tipo'),
                }

                if dados_form['tipo_id'] == '2' and not usuario.notificacoes:
                    messages.success(request, u"Não é possível enviar SMS Marketing para esse cliente")
                    return redirect(reverse('cadastro:detalhes', kwargs={'id': id}))

                Mensagem(**dados_form).save()

                messages.success(request, "Mensagem enviada com sucesso, confira o status do envio.")
                return redirect(reverse('cadastro:detalhes', kwargs={'id': id}))

    else:
        form = MensagemParticularForm()

    mensagens = Mensagem.objects.filter(usuario=id)[:30]
    for mensagem in mensagens:
        mensagem.atualiza_status()

    dados = {
                'cliente': usuario,
                'form': form,
                'mensagens_padrao': MensagemPadrao.objects.all(),
                'mensagens': mensagens,
                'menu': "menu_clientes",
    }

    return render(request, 'clientes/detalhes.html', dados)

@login_required(login_url='/login/')
def importar_planilha(request):

    dados = {'titulo': u'Importar Planilha',}

    if request.method == 'POST':
        form = ImportPlanilhaForm(request.POST, request.FILES)
        if form.is_valid():

            handle_uploaded_file(request.FILES['arquivo'], "%s%s%s.csv" % (MEDIA_ROOT, '/planilhas/', datetime.date.today()))
            dados['total_importacoes'] = importa_arquivo_csv("%s%s%s.csv" %(MEDIA_ROOT, '/planilhas/', datetime.date.today()), request.POST.get('categoria'))

            if dados['total_importacoes']:
                messages.success(request, 'Planilha importada com sucesso! %s registros foram importados.' % dados['total_importacoes'])
            else:
                messages.error(request, 'Ocorrreu um erro, nenhum registro foi importado.', extra_tags='danger')

    else:
        form = ImportPlanilhaForm()

    dados['form'] = form
    dados['menu'] = 'menu_clientes'

    return render(request, 'clientes/importar_planilha.html', dados)

@login_required(login_url='/login/')
def nova_categoria(request):

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Cliente adicionando com sucesso!')
            form.save()
            return redirect(reverse('front:categorias'))

    else:
        form = CategoriaForm()

    return render(request, 'categorias/novo.html', {'titulo': u'Cadastrar Nova Categoria', 'form': form})

@login_required(login_url='/login/')
def editar_categoria(request, id):

    categoria = get_object_or_404(Categoria, pk=id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            messages.success(request, 'Cliente atualizado com sucesso!')
            form.save()
            return redirect(reverse('front:categorias'))
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categorias/novo.html', {'titulo': u'Editar Categoria', 'form': form, 'categoria': categoria, 'menu': "menu_clientes",})

@login_required(login_url='/login/')
def cancelar_categoria(request, id):

    categoria = get_object_or_404(Categoria, pk=id)

    if request.method == 'POST':
        Categoria.objects.filter(id=id).update(data_cancelamento=datetime.datetime.now())
        messages.success(request, 'Registro removido com sucesso!')
        return redirect(reverse('front:categorias'))

    return render(request, 'categorias/cancelar.html', {'categoria': categoria, 'titulo': u'Remover Categoria', 'menu': "menu_clientes",})
