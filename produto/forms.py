import json
from urllib.parse import urlencode

import requests
from django import forms
from django.core.paginator import Paginator

from core.controle import session_get_headers, tratar_error
from core.settings import URL_API

TIPO_CATEGORIA = (
    ('REVENDA','Produtos para revenda'),
    ('CONSUMO','Produtos para consumo'),
    ('INSUMOS','Insumos de produção'),
    ('IMOBILIZADO','Ativos imobilizado'),
    ('SERVICO','Serviços'),
)


class CategoriaForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    tipoProduto = forms.ChoiceField(choices=TIPO_CATEGORIA, initial='INDEFINIDO', label='Tipo', required=True)
    def __init__(self, *args, request=None, uuid=None, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        response = requests.get(URL_API + 'categoria/' + str(uuid), headers=session_get_headers(request))
        if response.status_code == 200:
            self.initial = response.json()

    def salvar(self, request, uuid=None):
        data = self.json()
        headers = session_get_headers(request)
        if uuid:
            response = requests.patch(URL_API + 'categoria/' + str(uuid), json=data, headers=headers)
        else:
            response = requests.post(URL_API + 'categoria', json=data, headers=headers)
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

class CategoriaListForm(forms.Form):
    lista = []
    sort = forms.CharField()
    page = forms.IntegerField(initial=0)
    size = forms.IntegerField(initial=5)
    descricao = forms.CharField(label='Pesquisa', required=False,
                                widget=forms.TextInput(
                                    attrs={'autofocus': 'autofocus', 'placeholder': 'digite um valor para pesquisa'}))
    def pesquisar(self, request):
        itens_por_pagina = 3
        data = dict(request.GET or request.POST)
        params = {
            'page': data.get('page', 2),
            'size': data.get('size', itens_por_pagina),
            'sort': data.get('sort', 'descricao')+",asc",
            'descricao': data.get('descricao')
        }
        headers = session_get_headers(request)
        response = requests.get(URL_API + 'categoria', headers=headers, params=params)
        if response.status_code == 200:
            self.initial = dict(response.json())
            print(self.initial)
            page = {
                'object_list': self.initial.get('content'),
                'has_other_pages': self.initial.get('totalPages', 0) > 0,
                'has_previous': not self.initial.get('first'),
                'has_next': not self.initial.get('last'),
                'next_page_number': self.initial.get('number') + 1,
                'previous_page_number': self.initial.get('number') - 1
            }
            return page



