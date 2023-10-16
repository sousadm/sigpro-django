import json

import requests
from django import forms
from django.contrib import messages
from django.shortcuts import render
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error
from core.paginacao import get_page, get_param

from django.urls import reverse
from django.http import HttpResponseRedirect
from core.settings import URL_API
from core.tipos import TIPO_SITUACAO

URL_RECURSO = URL_API + 'caixa/'

TIPO_MOVIMENTO = (
    ('PAGAR', 'Conta Pagar'),
    ('RECEBER', 'Conta Receber'),
)

class CaixaForm(forms.Form):
    caixaId = forms.IntegerField(label='ID', required=False)
    usuarioId = forms.IntegerField(label='Usuário')
    tipo = forms.ChoiceField(choices=TIPO_MOVIMENTO, initial='RECEBER', label='Tipo Movimento')
    nominal = forms.CharField(max_length=100, label='Nominal')
    documento = forms.CharField(max_length=20, label='Documento')
    resumo = []
    valores = []
    titulos = []

    def __init__(self, *args, request=None, uuid=None, **kwargs):
        super(CaixaForm, self).__init__(*args, **kwargs)
        response = requests.get(URL_RECURSO + str(uuid), headers=session_get_headers(request))
        if response.status_code == 200:
            data = dict(response.json())
            self.initial = response.json()

    def salvar(self, request, uuid=None):
        data = dados_para_json(self.data)
        headers = session_get_headers(request)
        if uuid:
            response = requests.patch(URL_RECURSO + str(uuid), json=data, headers=headers)
        else:
            response = requests.post(URL_RECURSO, json=data, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()['caixaId'], response.status_code
        else:
            raise Exception(tratar_error(response))


@require_token
def caixaNew(request):
    return caixa_render(request, None)


def caixaEdit(request, uuid):
    return caixa_render(request, uuid)


@require_token
def caixa_render(request, uuid=None):
    template_name = 'financeiro/caixa_edit.html'
    try:
        if request.POST.get('btn_salvar'):
            form = CaixaForm(request.POST, request=request)
            uuid, status_code = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados' )
            if status_code == 201: 
                return HttpResponseRedirect(reverse('url_caixa_edit', kwargs={'uuid': uuid}))

        form = CaixaForm(request=request, uuid=uuid)
        
    except Exception as e:
        messages.error(request, e)

    return render(request, template_name, {'form': form})
