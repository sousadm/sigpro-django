import requests
from django import forms
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from core.controle import session_get_headers, tratar_error, dados_para_json, require_token
from core.settings import URL_API
from produto.distribuicao import centroDistribuicaoChoices

URL_RECURSO = URL_API + 'estoque/'

TIPO_ESTOQUE_MOVIMENTO = (
    ('ENTRADA', 'Entrada'),
    ('SAIDA', 'Saída'),
    ('TRANSFERENCIA', 'Transferência'),
)

class EstoqueForm(forms.Form):
    descricao = forms.CharField(label='Descrição do Produto', disabled=True, required=False)
    estoque = forms.DecimalField(label="Estoque atual", disabled=True, required=False, min_value=0, decimal_places=2, initial=0)
    produtoId = forms.IntegerField(label='Código do Produto', disabled=True)
    historico = forms.CharField(max_length=100, label='Histórico de movimentação', required=True, widget=forms.DateInput(attrs={'autofocus': 'true',}))
    documento = forms.CharField(max_length=10, label='Documento', required=False)
    quantidade = forms.DecimalField(label="Quantidade", min_value=0, decimal_places=2)
    centroDistribuicaoId = forms.ChoiceField(label='Centro de Distribuição', required=True, initial=None)
    centroDistribuicaoDestinoId = forms.ChoiceField(label='Centro de Distribuição Destinatário', required=True, initial=None)
    tipo = forms.ChoiceField(choices=TIPO_ESTOQUE_MOVIMENTO, label='Tipo de Movimentação', initial='ENTRADA')

    def __init__(self, *args, request, uuid=None, **kwargs):
        super(EstoqueForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].initial = TIPO_ESTOQUE_MOVIMENTO[0][0]
        self.fields['centroDistribuicaoId'].choices = centroDistribuicaoChoices(request)
        self.fields['centroDistribuicaoDestinoId'].choices = self.fields['centroDistribuicaoId'].choices

        if uuid:
            response = requests.get(URL_API + 'produto/' + str(uuid), headers=session_get_headers(request))
            data = dict(response.json())
            if response.status_code == 200:
                self.fields['descricao'].initial = data.get('descricao')
                self.fields['produtoId'].initial = data.get('id')
                self.fields['estoque'].initial = data.get('estoque', 0)
            else:
                raise Exception(tratar_error(response))

    def salvar(self, request, uuid=None):
        data = dados_para_json(self.data)
        if not (data.get('tipo') == 'TRANSFERENCIA'): data.pop('centroDistribuicaoDestinoId', None)
        headers = session_get_headers(request)
        if uuid:
            response = requests.post(URL_RECURSO, json=data, headers=headers)
            if response.status_code in [200, 201]:
                return response.json()['produtoId']
            else:
                raise Exception(tratar_error(response))
            

@require_token
def produtoEstoque(request, uuid):
    template_name = 'produto/produto_estoque.html'
    try:
        if request.POST.get('btn_salvar'):
            form = EstoqueForm(request.POST, request=request)
            form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')

    except Exception as e:
        messages.error(request, e)

    form = EstoqueForm(request=request, uuid=uuid)
    return render(request, template_name, {'form': form})

@require_token
def produtoEstoqueDetalhe(request, uuid):
    template_name = 'produto/produto_estoque_detalhe.html'
    response = requests.get(URL_API + 'produto/' + str(uuid) + '/estoque', headers=session_get_headers(request))
    return render(request, template_name, {'lista': response.json()})

