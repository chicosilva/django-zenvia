# -*- coding: utf-8 -*-

from django import forms
from mensagem.models import Mensagem, MensagemPadrao

OPCAO_ENVIO = (('', ''), ('todos', 'Enviar para Todos'), )

class MensagemUsuarioSelecaoForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = "__all__"

    todos = forms.ChoiceField(choices=OPCAO_ENVIO, required=False)

    def clean(self):

        if not self.cleaned_data.get('categoria') and not self.cleaned_data.get('bairro') and not self.cleaned_data.get('todos'):
            raise forms.ValidationError(u"Escolha um categoria, bairro ou opção de enviar para todos.")

        return self.cleaned_data

class MensagemUsuarioEspecificoForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = "__all__"

    usuarios = forms.CharField(label=u"Usuários", required=True)

class MensagemParticularForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = "__all__"

class MensagemCodigoPromocinalForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = "__all__"

    todos = forms.ChoiceField(choices=OPCAO_ENVIO, required=False)

    def __init__(self, *args, **kwargs):
        super(MensagemCodigoPromocinalForm, self).__init__(*args, **kwargs)
        self.fields['codigo_promocional'].required = True

    def clean(self):

        if not self.cleaned_data.get('categoria') and not self.cleaned_data.get('bairro') and not self.cleaned_data.get('todos'):
            raise forms.ValidationError(u"Escolha um categoria, bairro ou opção de enviar para todos.")

        return self.cleaned_data

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = "__all__"

    todos = forms.ChoiceField(choices=OPCAO_ENVIO, required=False)

    def __init__(self, *args, **kwargs):
        super(NoticiaForm, self).__init__(*args, **kwargs)
        self.fields['noticia'].required = True

    def clean(self):

        if not self.cleaned_data.get('categoria') and not self.cleaned_data.get('bairro') and not self.cleaned_data.get('todos'):
            raise forms.ValidationError(u"Escolha um categoria, bairro ou opção de enviar para todos.")

        return self.cleaned_data

class DetalheMensagemForm(forms.Form):
    resposta = forms.CharField(required=True, label='Resposta', widget=forms.Textarea)

class MensagemPadraoForm(forms.ModelForm):
    class Meta:
        model = MensagemPadrao
        fields = "__all__"
