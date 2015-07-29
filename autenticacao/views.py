# coding=utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from autenticacao.models import Configuracao, CustomUser
from django.contrib.auth.decorators import login_required
from autenticacao.forms import ConfiguracaoForm, FormEditarSenha, FormTermos
from django.contrib.auth.views import password_reset, password_reset_confirm

@login_required(login_url='/login/')
def termos(request):

    configuracao = Configuracao.objects.all().first()

    if request.method == 'POST':

        form = FormTermos(request.POST)

        if form.is_valid():
            configuracao.aceitou_termos = True
            configuracao.save()

            messages.success(request, 'Pronto! Faça o cadastro de seus clientes')
            return redirect(reverse('front:index'))
    else:
        form = FormTermos()

    dados = {
        'titulo': u'Termos de  Uso',
        'form': form,
        'menu': "menu_config",
    }
    return render(request, 'configuracoes/termos.html', dados)


def editar_senha(request):

    configuracao = get_object_or_404(CustomUser, pk=1)

    if request.method == 'POST':

        form_senha = FormEditarSenha(request.POST)

        if form_senha.is_valid():
            configuracao.password = make_password(request.POST.get('senha'))
            configuracao.save()

            messages.success(request, 'Senha alterada com sucesso!')
            return redirect(reverse('autenticacao:configuracoes'))
    else:
        form_senha = FormEditarSenha()

    dados = {
        'titulo': u'Editar Configurações',
        'form': ConfiguracaoForm(),
        'form_senha': form_senha,
        'configuracao': configuracao,
        'menu': "menu_config",
    }
    return render(request, 'configuracoes/detalhes.html', dados)

@login_required(login_url='/login/')
def configuracoes(request):

    configuracao = get_object_or_404(Configuracao, pk=1)

    if request.method == 'POST':
        form = ConfiguracaoForm(request.POST, instance=configuracao)
        if form.is_valid():
            messages.success(request, 'Dados atualizado com sucesso!')
            form.save()
            return redirect(reverse('autenticacao:configuracoes'))

        print form.errors

    else:
        form = ConfiguracaoForm(instance=configuracao)

    dados = {
        'titulo': u'Editar Configurações',
        'form': form,
        'form_senha': FormEditarSenha(),
        'configuracao': configuracao,
        'menu': "menu_config",
    }

    return render(request, 'configuracoes/detalhes.html', dados)

def entrar(request):

    if request.user.pk: return redirect(reverse('front:index'))

    if request.POST:
        username = request.POST.get('email', False)
        password = request.POST.get('senha', False)

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                return redirect(reverse('front:index'))

        messages.success(request, 'Usuário ou senha incorretos.')

    return render(request, 'autenticacao/login.html', {})

def sair(request):
    logout(request)
    return redirect(reverse('autenticacao:login'))

def restaurar_senha(request, uidb64=None, token=None):

    if request.method == 'POST':
        messages.success(request, u'Senha alterada com sucesso!')

    return password_reset_confirm(request, template_name='autenticacao/reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('autenticacao:login'))

def reset(request):

    if request.method == 'POST': messages.success(request, u'Um link com orientações para gerar uma nova senha foi enviada para seu e-mail')

    return password_reset(request, template_name='autenticacao/reset.html',
        email_template_name='autenticacao/reset_email.html',
        subject_template_name='autenticacao/reset_subject.txt',
        post_reset_redirect=reverse('autenticacao:login'))