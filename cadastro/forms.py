# -*- coding: utf-8 -*-

from django import forms
from cadastro.models import Categoria, Usuario, celular_to_int

class ImportPlanilhaForm(forms.Form):
    arquivo = forms.FileField(label='Selelcione um arquivo .csv')
    categoria = forms.ChoiceField(label="Categora", choices=(), initial=1, widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ImportPlanilhaForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].choices = [(pt.id, unicode(pt)) for pt in Categoria.objects.all()]

    def clean_arquivo(self):
        file = "%s" % self.cleaned_data['arquivo']
        extension = file[-4:]
        if extension != '.csv': raise forms.ValidationError("O arquivo deve ser.csv")

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"

    celular = forms.CharField(label="Celular", required=True)

    def clean_celular(self):

        if not celular_to_int(self.cleaned_data['celular']): raise forms.ValidationError(u"Formato Inválido.")

        return celular_to_int(self.cleaned_data['celular'])

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"

class RemoverNumeroForm(forms.Form):
    celular = forms.CharField(required=True, label='Celular')

    def clean_celular(self):

        if self.cleaned_data.get('celular'):
            celular = celular_to_int(self.cleaned_data['celular'])

            usuario = Usuario.objects.filter(celular=celular).count()

            if not usuario:
                raise forms.ValidationError(u"Número não encontrado em nossos registros.")

        return celular_to_int(self.cleaned_data['celular'])