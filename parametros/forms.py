from django import forms
from .models import *


class ParametroForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = '__all__'

class EmpleadoForm(forms.ModelForm):
    pass