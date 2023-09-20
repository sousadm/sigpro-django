import requests
from django.urls import reverse
from django import forms
from django.contrib import messages
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error
from django.shortcuts import render
from django.http import HttpResponseRedirect

from core.settings import URL_API

URL_RECURSO = URL_API + 'venda/'

STATUS_VENDA = (
    ('ORCAMENTO','Orçamento'),
    ('PEDIDO','Pedido'),
    ('CANCELADO','Cancelado'),
)

class VendaForm(forms.Form):
    vendaId = forms.IntegerField(label='ID', required=False)
    vendedorId = forms.IntegerField(label='Vendedor', required=False)
    vendedorNome = forms.CharField(max_length=100, label='Vendedor')
    VendaStatus = forms.ChoiceField(choices=STATUS_VENDA, label='Tipo', required=True, initial='ORCAMENTO')
    nome = forms.CharField(max_length=100, label='Nome do Cliente', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    documento = forms.CharField(max_length=14, label='CPF/CNPJ', required=True)
    fone = forms.CharField(max_length=20, label='Fone/Celular', required=True)
    email = forms.EmailField(max_length=254, label='E-mail', required=False)
    produtoId = forms.IntegerField(label='Produto', required=False)
    descricaoItem = forms.CharField(max_length=100, label='Descrição do produto', disabled=True, required=False)
    quantidade = forms.IntegerField(label='Quantidade', initial=1)
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

    def salvar(self, request, uuid=None):
        data = dados_para_json(self.data, [])
        raise Exception(data)
        # headers = session_get_headers(request)
        # if uuid:
        #     response = requests.patch(URL_RECURSO + str(uuid), json=data, headers=headers)
        # else:
        #     response = requests.post(URL_RECURSO, json=data, headers=headers)
        # if response.status_code in [200, 201]:
        #     return response.json()['vendaId']
        # else:
            # raise Exception(tratar_error(response))

    def testar(self):
        print('AKI DEU CERTO E SEMPRE:')


@require_token
def vendaNew(request):
    return venda_render(request, None)

@require_token
def vendaEdit(request, uuid):
    return venda_render(request, uuid)        

@require_token
def venda_render(request, uuid=None):
    form = VendaForm(request=request)
    template_name = 'venda/venda_edit.html'
    try:
        if request.POST:
            messages.success(request, request.POST)
            # form = VendaForm(request.POST, request=request)
            # uuid = form.salvar(request, uuid)
            # messages.success(request, 'sucesso ao gravar dados')
            # return HttpResponseRedirect(reverse('url_venda_edit', kwargs={'uuid': uuid}))
        
        form = VendaForm(request=request, uuid=uuid)
    except Exception as e:
        messages.error(request, e)
    context = {'form': form}
    return render(request, template_name, context)