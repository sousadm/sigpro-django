import json
import requests
from django import forms
from core.controle import session_get_headers, tratar_error
from core.paginacao import get_page, get_param
from core.settings import URL_API

URL_RECURSO = "precificacao"

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

    def __init__(self, *args, request=None, uuid=None, **kwargs):
        super(PrecificacaoForm, self).__init__(*args, **kwargs)
        response = requests.get(URL_API + 'precificacao/' + str(uuid), headers=session_get_headers(request))
        if response.status_code == 200:
            self.initial = response.json()

    def salvar(self, request, uuid=None):
        data = self.json()
        headers = session_get_headers(request)
        if uuid:
            response = requests.patch(URL_API + 'precificacao/' + str(uuid), json=data, headers=headers)
        else:
            response = requests.post(URL_API + 'precificacao', json=data, headers=headers)
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
        response = requests.get(URL_API + URL_RECURSO, headers=headers, params=params)
        if response.status_code == 200:
            self.fields['descricao'].initial = self.initial.get('descricao')
            self.initial = dict(response.json())
            return get_page(self.initial, params)
