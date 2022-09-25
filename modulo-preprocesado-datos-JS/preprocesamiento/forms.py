from django import forms

class FilesForm(forms.Form):
    planta = forms.FileField()
    nomina = forms.FileField()
    novedades = forms.FileField()


class LoginForm(forms.Form):
    user = forms.CharField(max_length=50)
    passwd = forms.CharField(max_length=50)