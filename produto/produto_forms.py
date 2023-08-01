import requests
from django import forms

from core.controle import session_get_headers
from core.settings import URL_API
from produto.categoria_views import categoriaChoices
from produto.models import TIPO_UNIDADE_MEDIDA
from produto.precificacao_views import precificacaoChoices


class ProdutoForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    ncm = forms.CharField(max_length=10, label='NCM')
    cest = forms.CharField(max_length=10, label='CEST')
    unidade = forms.ChoiceField(choices=TIPO_UNIDADE_MEDIDA, initial='UNID', label='Unidade')
    categoriaId = forms.ChoiceField(label='Categoria')
    precificacaoId = forms.ChoiceField(label='Precificação')
    precoCompra = forms.DecimalField(initial=0, decimal_places=2, label='Preço de Compra')
    precoVenda = forms.DecimalField(initial=0, decimal_places=2, label='Preço de Venda')
    estoque = forms.FloatField(initial=0, label='Estoque', disabled=True)

    def __init__(self, *args, request, uuid=None, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['categoriaId'].choices = categoriaChoices(request)
        self.fields['precificacaoId'].choices = precificacaoChoices(request)
        response = requests.get(URL_API + 'produto/' + str(uuid), headers=session_get_headers(request))
        if response.status_code == 200:
            self.initial = response.json()

class ProdutoListForm(forms.Form):
    descricao = forms.CharField(label='Pesquisa', required=False,
                                widget=forms.TextInput(
                                    attrs={'autofocus': 'autofocus', 'placeholder': 'digite um valor para pesquisa'}))
    def pesquisar(self, request):
        return None

