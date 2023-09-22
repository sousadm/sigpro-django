import requests
from django.urls import reverse
from django import forms
from django.contrib import messages
from core.controle import dados_para_json, require_token, session_get, session_get_headers, tratar_error
from django.shortcuts import render
from django.http import HttpResponseRedirect

from core.settings import URL_API

URL_RECURSO = URL_API + 'venda/'
URL_RECURSO_ITEM = URL_API + 'vendaitem/'

STATUS_VENDA = (
    ('ORCAMENTO','Orçamento de Venda'),
    ('PEDIDO','Pedido de Venda'),
    ('CANCELADO','Cancelado'),
)

class VendaForm(forms.Form):
    vendaId = forms.IntegerField(label='ID', required=False)
    vendedorId = forms.IntegerField(label='Vendedor', required=False)
    vendedorNome = forms.CharField(max_length=100, label='Vendedor', disabled=True)
    status = forms.ChoiceField(choices=STATUS_VENDA, label='Tipo', required=True, initial='ORCAMENTO')
    nome = forms.CharField(max_length=100, label='Nome do Cliente', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    documento = forms.CharField(max_length=14, label='CPF/CNPJ', required=True)
    fone = forms.CharField(max_length=20, label='Fone/Celular', required=True)
    email = forms.EmailField(max_length=254, label='E-mail', required=False)
    produtoId = forms.IntegerField(label='Produto')
    descricaoItem = forms.CharField(max_length=100, label='Descrição do produto', disabled=True, required=False)
    quantidade = forms.IntegerField(label='Quantidade', initial=1)
    preco = forms.DecimalField(label="Pr.Unit", min_value=0, decimal_places=2, initial=0, disabled=True)
    valorItem = forms.DecimalField(label="Valor Itens", min_value=0, decimal_places=2, initial=0, disabled=True)
    items = []

    def __init__(self, *args, request, uuid=None, **kwargs):         
        super(VendaForm, self).__init__(*args, **kwargs)
        if uuid:
            response = requests.get(URL_RECURSO + str(uuid), headers=session_get_headers(request))
            if response.status_code == 200:
                data = dict(response.json())
                self.initial = data
                self.items = data.get('items')
                self.orcamentos = data.get('orcamentos')
            else:
                raise Exception(tratar_error(response))
        else:
            vendedor = session_get(request, 'vendedorId')
            if vendedor:
                self.initial['vendedorId'] = vendedor
                self.initial['vendedorNome'] = session_get(request, 'nome')
                self.initial['nome'] = 'CLIENTE TESTE INICIAL'
                self.initial['fone'] = '85-94453322'

    def titulo(self):
        for status, titulo in STATUS_VENDA:
            if status == self.initial.get('status'):
                return titulo

    def salvar(self, request, uuid=None):
        data = dict(dados_para_json(self.data, []))    
        if data.get('produtoId'):
            item = {
                'produtoId': data.get('produtoId'),
                'quantidade': data.get('quantidade'),
            }
            data['items'] = [item]
            data.pop('produtoId', None)
            data.pop('quantidade', None)
            
        headers = session_get_headers(request)
        if uuid:
            response = requests.patch(URL_RECURSO + str(uuid), json=data, headers=headers)
        else:
            response = requests.post(URL_RECURSO, json=data, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()['vendaId']
        else:
            raise Exception(tratar_error(response))


@require_token
def vendaNew(request):
    return venda_render(request, None)

@require_token
def vendaEdit(request, uuid):
    return venda_render(request, uuid)        

@require_token
def venda_render(request, uuid=None):
    form = VendaForm(request=request, uuid=uuid)
    template_name = 'venda/venda_edit.html'
    try:
        if request.POST:
            form = VendaForm(request.POST, request=request)
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
            return HttpResponseRedirect(reverse('url_venda_edit', kwargs={'uuid': uuid}))
        
        form = VendaForm(request=request, uuid=uuid)
    except Exception as e:
        messages.error(request, e)
    context = {'form': form}
    return render(request, template_name, context)


@require_token
def removeVendaItem(request, uuid):
    params = {'id': uuid}
    headers = session_get_headers(request)
    response = requests.delete(URL_RECURSO_ITEM, headers=headers, params=params)
    if not response.status_code in [200, 201]:
        raise Exception(tratar_error(response))
    
