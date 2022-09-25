from django import forms

class FilesForm(forms.Form):
    planta = forms.FileField()
    nomina = forms.FileField()
    novedades = forms.FileField()
