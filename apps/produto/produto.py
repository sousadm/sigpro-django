from http.client import HTTPResponse
import json

import requests
from django import forms
from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse

from django.urls import reverse
from django.http import HttpResponseRedirect
from core.controle import session_get_headers, tratar_error, dados_para_json, require_token
from core.paginacao import get_param, get_page
from core.settings import URL_API
from apps.produto.categoria import categoriaChoices
from apps.produto.models import TIPO_UNIDADE_MEDIDA
from apps.produto.precificacao import precificacaoChoices

TIPO_NEGOCIAVEL = (
    ('True', 'Permite negociação de preço'),
    ('False', 'Preço de venda inegociável'),
)

URL_RECURSO = URL_API + 'produto/'

class ProdutoForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição', widget=forms.DateInput(attrs={'autofocus': 'true', }), initial='')
    unidade = forms.ChoiceField(choices=TIPO_UNIDADE_MEDIDA, label='Unidade', initial='UNID')
    precoCompra = forms.DecimalField(decimal_places=2, label='Preço de Compra', initial=0)
    precoVenda = forms.DecimalField(decimal_places=2, label='Preço de Venda', initial=0)
    precoSugerido = forms.DecimalField(decimal_places=2, label='Preço Sugerido', initial=0, disabled=True)
    estoque = forms.FloatField(initial=0, label='Estoque', disabled=True)
    categoriaId = forms.ChoiceField(label='Categoria', initial=None)
    precificacaoId = forms.ChoiceField(label='Precificação', initial=None)
    ncm = forms.CharField(max_length=10, label='NCM', initial=None)
    cest = forms.CharField(max_length=10, label='CEST', required=False, initial=None)
    negociavel = forms.ChoiceField(choices=TIPO_NEGOCIAVEL, label='Quanto Negociação', initial=False)
    
    def __init__(self, *args, request, uuid=None, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['categoriaId'].choices = categoriaChoices(request)
        self.fields['precificacaoId'].choices = precificacaoChoices(request)
        if uuid:
            response = requests.get(URL_API + 'produto/' + str(uuid), headers=session_get_headers(request))
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
            return response.json()['id'], response.status_code
        else:
            raise Exception(tratar_error(response))
        
    def atualizarEstoqueProduto(self, request, uuid):
        response = requests.post(URL_API + 'produto/' + str(uuid) + '/atualizar-estoque', headers=session_get_headers(request))
        if not response.status_code in [200, 201]:
            raise Exception(tratar_error(response))            


class ProdutoListForm(forms.Form):
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
def produtoNew(request):
    return produto_render(request, None)

@require_token
def produtoEdit(request, uuid):
    return produto_render(request, uuid)

@require_token
def produto_render(request, uuid=None):
    form = ProdutoForm(request=request)
    template_name = 'produto/produto_edit.html'
    try:

        if request.POST.get('btn_atualizar'):
            form.atualizarEstoqueProduto(request, uuid)
            messages.success(request, 'sucesso ao atualizar o estoque')

        if request.POST.get('btn_salvar'):
            form = ProdutoForm(request.POST, request=request)
            uuid, status_code = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados' )
            if status_code == 201: 
                return HttpResponseRedirect(reverse('url_produto_edit', kwargs={'uuid': uuid}))

        form = ProdutoForm(request=request, uuid=uuid)

    except Exception as e:
        messages.error(request, e)
    return render(request, template_name, {'form': form})


@require_token
def produtoList(request):
    template_name = 'produto/produto_list.html'
    try:
        form = ProdutoListForm() \
            if request.POST.get('btn_listar') \
            else ProdutoListForm(request.POST)
        page = form.pesquisar(request)

    except Exception as e:
        messages.error(request, e)
    context = {
        'form': form,
        'page': page
    }
    return render(request, template_name, context)


@require_token
def get_produto(request, uuid):
    headers = session_get_headers(request)
    response = requests.get(URL_RECURSO + str(uuid), headers=headers)
    return JsonResponse(response.json())


@require_token
def produtoPesquisa(request):
    template_name = 'produto/produto_pesquisa.html'
    form = ProdutoListForm(request.POST)
    page = form.pesquisar(request)
    context = {
        'form': form,
        'page': page
    }
    return render(request, template_name, context)





