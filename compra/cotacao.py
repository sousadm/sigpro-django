import json

import requests
from django import forms

from core.settings import URL_API

# Create your views here.

URL_COTACAO = URL_API + 'cotacao/'

class ProdutoForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    usuarioId = forms.IntegerField(label='Usuário', required=False)
    usuario = forms.CharField(label='Usuário')
    observacao = forms.CharField(max_length=100, label='Observação', widget=forms.DateInput(attrs={'autofocus': 'true', }), initial='')
        


    