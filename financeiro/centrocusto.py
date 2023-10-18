import json

import requests
from django import forms
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error
from core.paginacao import get_page, get_param

from core.settings import URL_API
from core.tipos import TIPO_SITUACAO

URL_RECURSO = URL_API + 'centrocusto/'

TIPO_FLUXO_CAIXA = (
    ('RECEITA', 'Receita'),
    ('FIXO', 'Custo Fixo'),
    ('VARIAVEL', 'Custo Variável'),
    ('INVESTIMENTO', 'Investimento'),
)

TIPO_MOVIMENTO = (
    ('PAGAR', 'Conta a Pagar'),
    ('RECEBER', 'Conta a Receber'),
)

class CentroCustoForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    fluxoCaixa = forms.ChoiceField(choices=TIPO_FLUXO_CAIXA, label='Tipo de Fluxo')
    tipoMovimento = forms.ChoiceField(choices=TIPO_MOVIMENTO, label='Tipo de Movimento')
    situacao = forms.ChoiceField(choices=TIPO_SITUACAO, initial=True)

    def __init__(self, *args, request=None, uuid=None, **kwargs):
        super(CentroCustoForm, self).__init__(*args, **kwargs)
        response = requests.get(URL_RECURSO + str(uuid), headers=session_get_headers(request))
        if response.status_code == 200:
            self.initial = response.json()    

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
def centrocustoNew(request):
    return centrocusto_render(request, None)


def centrocustoEdit(request, uuid):
    return centrocusto_render(request, uuid)


@require_token
def centrocusto_render(request, uuid=None):
    template_name = 'financeiro/centrocusto_edit.html'
    try:
        if request.POST.get('btn_salvar'):
            form = CentroCustoForm(request.POST, request=request)
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')

    except Exception as e:
        messages.error(request, e)

    form = CentroCustoForm(request=request, uuid=uuid)
    return render(request, template_name, {'form': form})


@require_token
def get_centrocusto_uuid(request, uuid):
    try:
        headers = session_get_headers(request)
        response = requests.get(URL_RECURSO + str(uuid), headers=headers, params={})
        data = dict(response.json())
        # return JsonResponse(data.get('content')[0])
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({})



@require_token
def centrocustoChoices(request):
    items = []
    response = requests.get(URL_RECURSO, headers=session_get_headers(request))
    if response.status_code == 200:
        for n in response.json()['content']:
            items.append((n['id'], n['descricao']))
    return items



@require_token
def centrocustoPesquisa(request):
    template_name = 'financeiro/centrocusto_pesquisa.html'
    params = {'sort':'nome,asc'}
    form = CentroCustoListForm(request.POST)
    page = form.pesquisar(request, params)
    return render(request, template_name, {'form': form, 'page': page})



class CentroCustoListForm(forms.Form):
    descricao = forms.CharField(label='Pesquisa', required=False,
                                widget=forms.TextInput(
                                    attrs={'autofocus': 'autofocus', 'placeholder': 'digite um valor para pesquisa'}))
    def pesquisar(self, request):
        itens_por_pagina = 5
        self.initial = request.POST or request.GET
        params = get_param(self.initial, itens_por_pagina)
        if self.initial.get('descricao'): 
            params['descricao'] = self.initial.get('descricao')
        headers = session_get_headers(request)
        response = requests.get(URL_RECURSO, headers=headers, params=params)
        if response.status_code == 200:
            self.fields['descricao'].initial = self.initial.get('descricao')
            self.initial = dict(response.json())
            return get_page(self.initial, params)


@require_token
def centrocustoList(request):
    template_name = 'financeiro/centrocusto_list.html'
    try:
        form = CentroCustoListForm() \
            if request.POST.get('btn_listar') \
            else CentroCustoListForm(request.POST)
        page = form.pesquisar(request)

    except Exception as e:
        messages.error(request, e)
        
    context = {'form': form, 'page': page}
    return render(request, template_name, context)
