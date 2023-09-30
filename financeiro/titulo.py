import json

import requests
from django import forms
from django.contrib import messages
from django.shortcuts import render
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error
from core.paginacao import get_page, get_param

from core.settings import URL_API
from core.tipos import TIPO_SITUACAO

URL_RECURSO = URL_API + 'titulo/'

TIPO_DOCUMENTO = (
    ('DINHEIRO', 'dinheiro'),
    ('CREDITO', 'crédito'),
    ('DEBITO', 'débito'),
    ('BOLETO', 'boleto'),
    ('DEPOSITO', 'depósito'),
    ('CHEQUE', 'cheque'),
    ('OUTROS', 'outros'),
    ('PROMISSORIA', 'promissória'),
    ('PIX', 'pix'),
    ('CARTEIRA', 'carteira'),
)


class TituloForm(forms.Form):
    tituloId = forms.IntegerField(label='ID', required=False)
    participanteId = forms.IntegerField(label='Participante')
    centroCustoId = forms.IntegerField(label='Centro Custo')
    centroCusto = forms.CharField(
        max_length=100, label='Centro de Custo', disabled=True, required=True)
    participante = forms.CharField(
        max_length=100, label='Participante', disabled=True, required=True)
    historico = forms.CharField(max_length=100, label='Histórico', widget=forms.DateInput(
        attrs={'autofocus': 'true', }))
    documento = forms.CharField(max_length=20, label='Documento')
    portador = forms.ChoiceField(
        choices=TIPO_DOCUMENTO, initial='BOLETO', label='Portador')
    created_dt = forms.DateTimeField(
        label='Dt.Cadastro', required=False, disabled=True)
    updated_dt = forms.DateTimeField(
        label='Dt.Atualização', required=False, disabled=True)
    vencimento = forms.DateField(label='Vencimento',
                                 widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control', }))
    previsao_dt = forms.DateField(label='Dt.Previsão',
                                  widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control', }))
    baixa_dt = forms.DateField(label='Dt.Baixa', disabled=True, required=False,
                               widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control', }))
    valor = forms.DecimalField(label='Valor', decimal_places=2, initial=0)
    multa = forms.DecimalField(label='Multa %', decimal_places=2, initial=0,
                               widget=forms.DateInput(attrs={'title': 'percentual de multa sobre a parcela', }))
    juro = forms.DecimalField(label='Juro %', decimal_places=2, initial=0,
                              widget=forms.DateInput(attrs={'title': 'percentual de juro sobre a parcela por 30 dias', }))
    desconto = forms.DecimalField(label='Desconto R$', decimal_places=2, initial=0,
                                  widget=forms.DateInput(attrs={'title': 'desconto até o dia do vencimento', }))
    saldo = forms.DecimalField(label='Saldo', decimal_places=2, initial=0, disabled=True)
    modificado = forms.BooleanField()

    def __init__(self, *args, request=None, uuid=None, **kwargs):
        super(TituloForm, self).__init__(*args, **kwargs)
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
            return response.json()['tituloId']
        else:
            raise Exception(tratar_error(response))


class TituloListForm(forms.Form):
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
def tituloNew(request):
    return titulo_render(request, None)


def tituloEdit(request, uuid):
    return titulo_render(request, uuid)


@require_token
def titulo_render(request, uuid=None):
    template_name = 'financeiro/titulo_edit.html'
    try:
        if request.POST.get('btn_salvar'):
            form = TituloForm(request.POST, request=request)
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')

        form = TituloForm(request=request, uuid=uuid)
        
    except Exception as e:
        messages.error(request, e)

    return render(request, template_name, {'form': form})


@require_token
def tituloList(request):
    template_name = 'financeiro/titulo_list.html'
    try:
        form = TituloListForm() \
            if request.POST.get('btn_listar') \
            else TituloListForm(request.POST)
        page = form.pesquisar(request)

    except Exception as e:
        messages.error(request, e)

    return render(request, template_name, {'form': form, 'page': page})
