# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Configuracion

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = ['telefono_whatsapp']