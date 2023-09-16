from django.shortcuts import render

import requests
from django import forms
from django.contrib import messages
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error
from core.paginacao import get_page, get_param
from core.settings import URL_API
from venda.models import SITUACAO_CADASTRAL, TIPO_PAGAMENTO

# Create your views here.

URL_RECURSO = URL_API + 'formapgto/'

class FormaPgtoForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    tipoPagamento = forms.ChoiceField(choices=TIPO_PAGAMENTO, initial='DINHEIRO', label='Tipo de Pagamento', required=True)
    parcelas = forms.IntegerField(label='Parcelas', initial=1, min_value=1, max_value=24)
    descontoMaximo = forms.FloatField(label='Desconto', initial=0, min_value=0, max_value=100)
    valorMinimo = forms.FloatField(label='Mínimo', initial=0, min_value=0.01)
    prazoMedio = forms.FloatField(label='Prazo Médio de Pgto', initial=1, min_value=0.01)
    situacao = forms.ChoiceField(choices=SITUACAO_CADASTRAL, initial='ATIVO', label='Situação', widget=forms.DateInput(attrs={'title': 'situação cadastral', }))

    def __init__(self, *args, request=None, uuid=None, **kwargs):
        super(FormaPgtoForm, self).__init__(*args, **kwargs)
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
        

class FormaPgtoListForm(forms.Form):
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
def formaPgtoNew(request):
    return formaPgto_render(request, None)


def formaPgtoEdit(request, uuid):
    return formaPgto_render(request, uuid)


@require_token
def formaPgto_render(request, uuid=None):
    template_name = 'venda/formapgto_edit.html'
    try:
        if request.POST.get('btn_salvar'):
            form = FormaPgtoForm(request.POST, request=request)
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
    except Exception as e:
        messages.error(request, e)
    form = FormaPgtoForm(request=request, uuid=uuid)
    return render(request, template_name, {'form': form})


@require_token
def formapgtoList(request):
    template_name = 'venda/formapgto_list.html'
    try:
        form = FormaPgtoListForm() \
            if request.POST.get('btn_listar') \
            else FormaPgtoListForm(request.POST)
        page = form.pesquisar(request)

    except Exception as e:
        messages.error(request, e)
    context = {
        'form': form,
        'page': page
    }
    return render(request, template_name, context)


