from django import forms
from .models import *
##Formularios de empresas

class EmpresasCreateForm(forms.ModelForm):
    class Meta:
        model= Empresa
        fields = '__all__'

class ConceptoInternoForm(forms.ModelForm):
    class Meta:
        model = ConceptoInterno
        fields = '__all__'
