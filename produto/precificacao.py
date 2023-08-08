import json
import requests
from django import forms
from django.contrib import messages
from django.shortcuts import render

from core.controle import session_get_headers, tratar_error, require_token, dados_para_json
from core.paginacao import get_page, get_param
from core.settings import URL_API

URL_RECURSO = URL_API + "precificacao/"

class PrecificacaoForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição',
                                widget=forms.DateInput(attrs={'autofocus': 'true', }))
    agregado = forms.DecimalField(label="Agregado %", min_value=0, decimal_places=2, initial=0)
    frete = forms.DecimalField(label="Frete %", min_value=0, decimal_places=2, initial=0)
    imposto = forms.DecimalField(label="Imposto %", min_value=0, decimal_places=2, initial=0)
    credito = forms.DecimalField(label="Crédito %", min_value=0, decimal_places=2, initial=0)

    margemLucro = forms.DecimalField(label="Margem de Lucro %", min_value=0, decimal_places=2, initial=0)
    despesaFixa = forms.DecimalField(label="Despesa Fixa %", min_value=0, decimal_places=2, initial=0)
    despesaVariavel = forms.DecimalField(label="Despesa Variável %", min_value=0, decimal_places=2, initial=0)
    markup = forms.DecimalField(label="Fator Multiplicador", min_value=0, decimal_places=4, initial=0, disabled=True)

    def __init__(self, *args, request=None, uuid=None, **kwargs):
        super(PrecificacaoForm, self).__init__(*args, **kwargs)
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


class PrecificacaoListForm(forms.Form):
    descricao = forms.CharField(label='Pesquisa', required=False,
                                widget=forms.TextInput(
                                    attrs={'autofocus': 'autofocus', 'placeholder': 'digite um valor para pesquisa'}))

    def pesquisar(self, request):
        itens_por_pagina = 5
        self.initial = request.POST or request.GET
        params = get_param(self.initial, itens_por_pagina)
        if self.initial.get('descricao'): params['descricao'] = self.initial.get('descricao')
        headers = session_get_headers(request)
        response = requests.get(URL_RECURSO, headers=headers, params=params)
        if response.status_code == 200:
            self.fields['descricao'].initial = self.initial.get('descricao')
            self.initial = dict(response.json())
            return get_page(self.initial, params)


@require_token
def precificacaoNew(request):
    return precificacao_render(request, None)

def precificacaoEdit(request, uuid):
    return precificacao_render(request, uuid)


@require_token
def precificacao_render(request, uuid=None):
    template_name = 'produto/precificacao_edit.html'
    try:
        if request.POST.get('btn_salvar'):
            form = PrecificacaoForm(request.POST, request=request)
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
    except Exception as e:
        messages.error(request, e)
    form = PrecificacaoForm(request=request, uuid=uuid)
    return render(request, template_name, {'form': form})

@require_token
def precificacaoList(request):
    template_name = 'produto/precificacao_list.html'
    try:
        form = PrecificacaoListForm() \
            if request.POST.get('btn_listar') \
            else PrecificacaoListForm(request.POST)
        page = form.pesquisar(request)

    except Exception as e:
        messages.error(request, e)
    context = {
        'form': form,
        'page': page
    }
    return render(request, template_name, context)


@require_token
def precificacaoChoices(request):
    lista = []
    response = requests.get(URL_API + 'precificacao', headers=session_get_headers(request))
    if response.status_code == 200:
        for n in response.json()['content']:
            lista.append((n['id'], n['descricao']))
    return lista
