import json

import requests
from django import forms
from django.contrib import messages
from django.shortcuts import render

from django.urls import reverse
from django.http import HttpResponseRedirect
from core.controle import session_get_headers, tratar_error, require_token, dados_para_json
from core.paginacao import get_page, get_param
from core.settings import URL_API
from produto.models import TIPO_CATEGORIA

URL_RECURSO = URL_API + 'categoria/'

class CategoriaForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    tipoProduto = forms.ChoiceField(choices=TIPO_CATEGORIA, initial='INDEFINIDO', label='Tipo', required=True)
    def __init__(self, *args, request=None, uuid=None, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        response = requests.get(URL_RECURSO + str(uuid), headers=session_get_headers(request))
        if response.status_code == 200:
            self.initial = response.json()

    def salvar(self, request, uuid=None):
        data = dados_para_json(self.data)
        headers = session_get_headers(request)
        if uuid: response = requests.patch(URL_RECURSO + str(uuid), json=data, headers=headers)
        else: response = requests.post(URL_RECURSO, json=data, headers=headers)

        if response.status_code in [200, 201]:
            return response.json()['id'], response.status_code
        else:
            raise Exception(tratar_error(response))


class CategoriaListForm(forms.Form):
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
def categoriaNew(request):
    return categoria_render(request, None)


def categoriaEdit(request, uuid):
    return categoria_render(request, uuid)


@require_token
def categoria_render(request, uuid=None):
    form = CategoriaForm(request=request, uuid=uuid)
    template_name = 'produto/categoria_edit.html'
    try:
        if request.POST.get('btn_salvar'):
            form = CategoriaForm(request.POST, request=request)
            uuid, status_code = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_categoria_edit', kwargs={'uuid': uuid}))
            
    except Exception as e:
        messages.error(request, e)
        
    return render(request, template_name, {'form': form})


@require_token
def categoriaList(request):
    template_name = 'produto/categoria_list.html'
    try:
        form = CategoriaListForm() \
            if request.POST.get('btn_listar') \
            else CategoriaListForm(request.POST)
        page = form.pesquisar(request)

    except Exception as e:
        messages.error(request, e)
    context = {
        'form': form,
        'page': page
    }
    return render(request, template_name, context)


@require_token
def categoriaChoices(request):
    items = []
    response = requests.get(URL_RECURSO, headers=session_get_headers(request))
    if response.status_code == 200:
        for n in response.json()['content']:
            items.append((n['id'], n['descricao']))
    return items

