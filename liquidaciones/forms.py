from django import forms
from .models import *
##Formularios de empresas

class EmpresasCreateForm(forms.ModelForm):
    class Meta:
        model= Empresa
        fields = '__all__'