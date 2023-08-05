import json

import requests
from django import forms

from core.controle import session_get_headers, tratar_error
from core.settings import URL_API
from produto.categoria_views import categoriaChoices
from produto.models import TIPO_UNIDADE_MEDIDA
from produto.precificacao_views import precificacaoChoices

URL_RECURSO = URL_API + 'produto/'

class ProdutoForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição', widget=forms.DateInput(attrs={'autofocus': 'true', }), initial='PRODUTO TESTE')
    unidade = forms.ChoiceField(choices=TIPO_UNIDADE_MEDIDA, label='Unidade', initial='UNID')
    precoCompra = forms.DecimalField(initial=0, decimal_places=2, label='Preço de Compra')
    precoVenda = forms.DecimalField(decimal_places=2, label='Preço de Venda', disabled=True, initial=23.20)
    estoque = forms.FloatField(initial=0, label='Estoque', disabled=True)
    categoriaId = forms.ChoiceField(label='Categoria', initial=4)
    precificacaoId = forms.ChoiceField(label='Precificação', initial=1)
    ncm = forms.CharField(max_length=10, label='NCM', initial='111000111')
    cest = forms.CharField(max_length=10, label='CEST', initial='101010')
    def __init__(self, *args, request, uuid=None, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['categoriaId'].choices = categoriaChoices(request)
        self.fields['precificacaoId'].choices = precificacaoChoices(request)
        response = requests.get(URL_API + 'produto/' + str(uuid), headers=session_get_headers(request))
        if response.status_code == 200:
            self.initial = response.json()

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
        return None

