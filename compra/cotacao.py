import json

import requests
from django.contrib import messages
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from compra.cotacao_item import CotacaoItemForm
from compra.cotacao_orcamento import CotacaoOrcamentoForm
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error

from core.settings import URL_API
from produto.models import TIPO_UNIDADE_MEDIDA

# Create your views here.

URL_RECURSO = URL_API + 'cotacao/'

class CotacaoForm(forms.Form):
    cotacaoId = forms.IntegerField(label='ID', required=False)
    usuarioId = forms.IntegerField(label='Usuário', required=False)
    usuario = forms.CharField(label='Cotista', disabled=True, required=False)
    descricao = forms.CharField(max_length=100, label='Descrição da Cotação', widget=forms.DateInput(attrs={'autofocus': 'true', }), initial='TESTE INICIAL')
    created_dt = forms.DateTimeField(label='Data do cadastro', required=False, disabled=True)
    items = []
    orcamentos = []
        
    def __init__(self, *args, request, uuid=None, **kwargs):
        super(CotacaoForm, self).__init__(*args, **kwargs)
        if uuid:
            response = requests.get(URL_RECURSO + str(uuid), headers=session_get_headers(request))
            if response.status_code == 200:
                data = dict(response.json())
                self.initial = data
                self.items = data.get('items')
                self.orcamentos = data.get('orcamentos')
            else:
                raise Exception(tratar_error(response))

    def salvar(self, request, uuid=None):
        data = dados_para_json(self.data, ['usuarioId'])
        headers = session_get_headers(request)
        if uuid:
            response = requests.patch(URL_RECURSO + str(uuid), json=data, headers=headers)
        else:
            response = requests.post(URL_RECURSO, json=data, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()['id']
        else:
            raise Exception(tratar_error(response))
        

@require_token
def cotacaoNew(request):
    return cotacao_render(request, None)

@require_token
def cotacaoEdit(request, uuid):
    return cotacao_render(request, uuid)

@require_token
def cotacao_render(request, uuid=None):
    form = CotacaoForm(request=request)
    template_name = 'compra/cotacao_edit.html'
    try:
        if request.POST.get('btn_item_salvar'):
            cotacaoItemId = request.POST.get('cotacaoItemId')
            formItem = CotacaoItemForm(request.POST, request=request)
            formItem.salvar(request, cotacaoItemId=cotacaoItemId, cotacao=uuid)
            messages.success(request, 'sucesso ao gravar item')

        if request.POST.get('btn_orcamento_salvar'):
            orcamentoId = request.POST.get('orcamentoId')
            formOrcamento = CotacaoOrcamentoForm(request.POST, request=request)
            formOrcamento.salvar(request, uuid, orcamentoId)
            messages.success(request, 'sucesso ao gravar orçamento')            

        if request.POST.get('btn_salvar'):
            form = CotacaoForm(request.POST, request=request)
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_cotacao_edit', kwargs={'uuid': uuid}))

    except Exception as e:
        messages.error(request, e)

    form = CotacaoForm(request=request, uuid=uuid)
    context = {'form': form}
    return render(request, template_name, context)


