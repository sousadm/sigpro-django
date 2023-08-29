import requests
from django.contrib import messages
from django import forms
from django.shortcuts import render
from core.controle import require_token, session_get_headers
from core.settings import URL_API

from produto.models import TIPO_UNIDADE_MEDIDA

URL_RECURSO = URL_API + 'cotacao/'

class CotacaoItemForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    cotacaoId = forms.IntegerField(label='Cotação', required=False)
    produtoId = forms.IntegerField(label='Produto', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição do produto', initial='', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    unidade = forms.ChoiceField(choices=TIPO_UNIDADE_MEDIDA, label='Unidade', initial='UNID')
    quantidade = forms.IntegerField(label='Quantidade', initial=1)

    def __init__(self, *args, request, uuid=None, **kwargs):
        super(CotacaoItemForm, self).__init__(*args, **kwargs)
        # if uuid:
        #     response = requests.get(URL_RECURSO + str(uuid), headers=session_get_headers(request))
        #     if response.status_code == 200:
        #         self.initial = response.json()
        #     else:
        #         raise Exception(tratar_error(response))    

@require_token
def cotacaoItemNew(request, uuid):
    return cotacao_item_render(request=request, cotacao=uuid)

@require_token 
def cotacaoItemEdit(request, uuid):
    return cotacao_item_render(request, uuid, None)

@require_token
def cotacao_item_render(request, uuid=None, cotacao=None):
    form = CotacaoItemForm(request=request)
    template_name = 'compra/cotacao_item.html'
    try:
        form = CotacaoItemForm(request=request, uuid=uuid)
    except Exception as e:
        messages.error(request, e)

    return render(request, template_name, {'form': form})


