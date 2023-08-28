import json

import requests
from django.contrib import messages
from django import forms
from django.shortcuts import render
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error

from core.settings import URL_API

# Create your views here.

URL_RECURSO = URL_API + 'cotacao/'

class CotacaoForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    usuarioId = forms.IntegerField(label='Usuário', required=False)
    usuario = forms.CharField(label='Usuário')
    observacao = forms.CharField(max_length=100, label='Observação', widget=forms.DateInput(attrs={'autofocus': 'true', }), initial='')
        
    def __init__(self, *args, request, uuid=None, **kwargs):
        super(CotacaoForm, self).__init__(*args, **kwargs)
        if uuid:
            response = requests.get(URL_RECURSO + str(uuid), headers=session_get_headers(request))
            if response.status_code == 200:
                self.initial = response.json()
            else:
                raise Exception(tratar_error(response))

    def salvar(self, request, uuid=None):
        data = dados_para_json(self.data)
        headers = session_get_headers(request)
        if uuid:
            response = requests.patch(URL_RECURSO + str(uuid), json=data, headers=headers)
        else:
            response = requests.post(URL_RECURSO, json=data, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()['id']
        else:
            raise Exception(tratar_error(response))
        

@require_token
def cotacaoNew(request):
    return cotacao_render(request, None)

@require_token
def cotacaoEdit(request, uuid):
    return cotacao_render(request, uuid)

@require_token
def cotacao_render(request, uuid=None):
    form = CotacaoForm(request=request)
    template_name = 'compra/cotacao_edit.html'
    try:

        form = CotacaoForm(request=request, uuid=uuid)

    except Exception as e:
        messages.error(request, e)
    return render(request, template_name, {'form': form})


