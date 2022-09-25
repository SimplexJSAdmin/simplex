from django import forms
from .models import *
##Formularios de empresas

class EmpresasCreateForm(forms.ModelForm):
    class Meta:
        model= Empresa
        fields = '__all__'

class ConceptoInternoForm(forms.ModelForm):
    class Meta:
        model = ConceptoEmpresa
        fields = '__all__'

class FileForm(forms.ModelForm):
    class Meta:
        model = Preprocesamiento
        fields = ['nomina', 'novedades', 'planta']
