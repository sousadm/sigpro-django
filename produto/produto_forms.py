import json

import requests
from django import forms

from core.controle import session_get_headers, tratar_error
from core.paginacao import get_param, get_page
from core.settings import URL_API
from produto.categoria_views import categoriaChoices
from produto.models import TIPO_UNIDADE_MEDIDA
from produto.precificacao import precificacaoChoices

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
    cest = forms.CharField(max_length=10, label='CEST', initial=None)
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
        data = self.json()
        headers = session_get_headers(request)
        if uuid:
            response = requests.patch(URL_RECURSO + str(uuid), json=data, headers=headers)
        else:
            response = requests.post(URL_RECURSO, json=data, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()['id']
        else:
            raise Exception(tratar_error(response))

    def json(self):
        post_data = dict(self.data)
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        json_data = json.dumps(post_data).replace("[", "").replace("]", "")
        data = json.loads(json_data)
        return data

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

