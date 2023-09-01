import requests
from django.contrib import messages
from django import forms
from django.shortcuts import render
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error
from core.settings import URL_API

from produto.models import TIPO_UNIDADE_MEDIDA

URL_RECURSO = URL_API + 'cotacao/'

class CotacaoItemForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    cotacaoId = forms.IntegerField(
        label='Cotação', required=True, disabled=True)
    produtoId = forms.IntegerField(label='Produto', required=False)
    descricaoItem = forms.CharField(max_length=100, label='Descrição do produto',
                                    initial='PRODUTO TESTE', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    unidade = forms.ChoiceField(
        choices=TIPO_UNIDADE_MEDIDA, label='Unidade', initial='UNID')
    ncm = forms.CharField(label='NCM', initial='000000', max_length=10)
    quantidade = forms.IntegerField(label='Quantidade', initial=1)

    def __init__(self, *args, request, uuid=None, cotacao=None, **kwargs):
        super(CotacaoItemForm, self).__init__(*args, **kwargs)
        if cotacao:
            self.fields['cotacaoId'].initial = cotacao

    def salvar(self, request, uuid=None):
        data = dados_para_json(
            self.data, nones=['descricaoItem', 'usuarioId', 'btn_item_salvar'])
        data['descricao'] = self.data.get('descricaoItem')
        headers = session_get_headers(request)
        response = requests.post(
            URL_RECURSO + str(uuid) + "/item", json=data, headers=headers)
        if not response.status_code in [200, 201]:
            raise Exception(tratar_error(response))


@require_token
def cotacaoItemNew(request, uuid):
    return cotacao_item_render(request=request, cotacao=uuid)


@require_token
def cotacaoItemEdit(request, uuid):
    return cotacao_item_render(request, uuid, None)


@require_token
def cotacao_item_render(request, uuid=None, cotacao=None):
    template_name = 'compra/cotacao_item.html'
    form = CotacaoItemForm(request=request, uuid=uuid, cotacao=cotacao)
    return render(request, template_name, {'form': form})
