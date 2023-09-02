import requests
from django.contrib import messages
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error
from core.settings import URL_API

from produto.models import TIPO_UNIDADE_MEDIDA

URL_RECURSO = URL_API + 'cotacao/'
URL_RECURSO_ITEM = URL_API + 'cotacao-item/'

class CotacaoItemForm(forms.Form):
    cotacaoId = forms.IntegerField(label='Cotação', required=False)
    cotacaoItemId = forms.IntegerField(label='ID', required=False, disabled=True)
    produtoId = forms.IntegerField(label='Produto', required=False)
    descricaoItem = forms.CharField(max_length=100, label='Descrição do produto', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    unidade = forms.ChoiceField(choices=TIPO_UNIDADE_MEDIDA, label='Unidade')
    ncm = forms.CharField(label='NCM', max_length=10)
    quantidade = forms.IntegerField(label='Quantidade')

    def __init__(self, *args, request, uuid=None, cotacao=None, **kwargs):
        super(CotacaoItemForm, self).__init__(*args, **kwargs)
        if cotacao:
            self.fields['cotacaoId'].initial = cotacao
        response = requests.get(URL_RECURSO_ITEM + str(uuid), headers=session_get_headers(request))
        if response.status_code == 200:
            data = dict(response.json())
            self.initial = data

    def salvar(self, request, uuid=None, cotacaoItemId=None):
        data = dados_para_json(self.data, nones=['cotacaoItemId','descricao','usuarioId', 'btn_item_salvar'])
        headers = session_get_headers(request)
        if cotacaoItemId:
            response = requests.patch(URL_RECURSO_ITEM + str(cotacaoItemId), json=data, headers=headers)
        else:
            response = requests.post(URL_RECURSO + str(uuid) + "/item", json=data, headers=headers)
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

@require_token
def cotacaoItemDelete(request, uuid, item):
    response = requests.delete(URL_RECURSO_ITEM + str(item), headers=session_get_headers(request))
    if response.status_code == 200:
        messages.success(request, 'item excluído com sucesso')
    else:
        messages.error(request, Exception(tratar_error(response)))
    return HttpResponseRedirect(reverse('url_cotacao_edit', kwargs={'uuid': uuid}))
