# -*- coding: utf-8 -*-
from django import forms
from autenticacao.models import Configuracao, CustomUser

class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = Configuracao
        fields = "__all__"

class FormEditarSenha(forms.Form):

    senha_atual     = forms.CharField(label='Senha atual', max_length=100, widget=forms.PasswordInput(), required=True)
    senha           = forms.CharField(label='Nova Senha', max_length=100, widget=forms.PasswordInput(), required=True)
    confirme        = forms.CharField(label='Confirme sua Senha', max_length=100, widget=forms.PasswordInput(), required=True)

    def clean(self):

        user = CustomUser.objects.get(pk=1)

        if not user.check_password(self.cleaned_data.get('senha_atual')): raise forms.ValidationError(u"A senha atual não confere.")

        if self.cleaned_data.get('senha') != self.cleaned_data.get('confirme'): raise forms.ValidationError(u"As senhas devem ser iguais")
        return self.cleaned_data

class FormTermos(forms.Form):

    termos = forms.CharField(label='Aceita os termos?', widget=forms.CheckboxInput(), required=True)