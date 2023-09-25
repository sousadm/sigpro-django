import requests
from django.contrib import messages
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error
from core.settings import URL_API

from produto.models import TIPO_UNIDADE_MEDIDA

URL_RECURSO = URL_API + 'venda/'
URL_RECURSO_ITEM = URL_API + 'venda-item/'

class VendaItemForm(forms.Form):
    vendaId = forms.IntegerField(label='Cotação', required=False)
    itemId = forms.IntegerField(label='ID', required=False, disabled=True)
    produtoId = forms.IntegerField(label='Produto', required=False, disabled=True)
    descricaoItem = forms.CharField(max_length=100, label='Descrição do produto', disabled=True)
    unidade = forms.ChoiceField(choices=TIPO_UNIDADE_MEDIDA, label='Unidade', initial='UNID')
    ncm = forms.CharField(label='NCM', max_length=10, required=False)
    quantidade = forms.IntegerField(label='Quantidade', min_value=0)
    preco = forms.DecimalField(label="Pr.Unit", min_value=0, decimal_places=2, initial=0, disabled=True)
    descontoItem = forms.DecimalField(label="Desconto", min_value=0, decimal_places=2, initial=0)
    valorItem = forms.DecimalField(label="Valor do Item", min_value=0, decimal_places=2, initial=0, disabled=True)

    def __init__(self, *args, request, uuid=None, venda=None, **kwargs):
        super(VendaItemForm, self).__init__(*args, **kwargs)
        self.fields['itemId'].initial = uuid
        self.fields['vendaId'].initial = venda
        response = requests.get(URL_RECURSO_ITEM + str(uuid), headers=session_get_headers(request))
        if response.status_code == 200:
            data = dict(response.json())
            self.initial = data 

    def salvar(self, request, venda=None):    
        itemId = self.data.get('itemId')
        if not itemId: raise Exception('sem o identificador do item')
        dados = {
            'produtoId': self.data.get('produtoItemId'),
            'quantidade': self.data.get('quantidadeItem'),
            'descontoItem': self.data.get('descontoItem'),
        }
        headers = session_get_headers(request)
        response = requests.patch(URL_RECURSO_ITEM + str(itemId), json=dados, headers=headers)
        if not response.status_code in [200, 201]:
            raise Exception(tratar_error(response))


@require_token
def vendaItemNew(request, uuid):
    return venda_item_render(request=request, venda=uuid)


@require_token
def vendaItemEdit(request, uuid):
    return venda_item_render(request, uuid, None)


@require_token
def venda_item_render(request, uuid=None, venda=None):
    template_name = 'venda/venda_item.html'
    form = VendaItemForm(request=request, uuid=uuid, venda=venda)
    return render(request, template_name, {'form': form})


@require_token
def vendaItemDelete(request, uuid, item):
    response = requests.delete(URL_RECURSO_ITEM + str(item), headers=session_get_headers(request))
    if response.status_code == 200:
        messages.success(request, 'item excluído com sucesso')
    else:
        messages.error(request, Exception(tratar_error(response)))
    return HttpResponseRedirect(reverse('url_venda_edit', kwargs={'uuid': uuid}))
