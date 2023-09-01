import requests
from django.contrib import messages
from django import forms
from django.shortcuts import render
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error
from core.settings import URL_API
from produto.precificacao import precificacaoChoices

URL_RECURSO = URL_API + 'cotacao/'

TIPO_COTACAO_STATUS = (
	('EM_ANALISE', 'Em anállise'), 
    ('APROVADO', 'Aprovado'), 
    ('CANCELADO', 'Cancelado'),
)

class CotacaoOrcamentoForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    nome = forms.CharField(label='Nome do Fornecedor', max_length=100, initial='Casa da Borracha')
    documento = forms.CharField(label='Documento', max_length=14, required=False, widget=forms.DateInput(attrs={'title': 'digite o CPF ou CNPJ', }), initial='10101010101010')
    email = forms.EmailField(label='E-mail', initial='borracha@hot.com')
    fone = forms.CharField(label='Fone', max_length=20, initial='8599994400')
    desconto = forms.DecimalField(decimal_places=2, label='Desconto', initial=0)
    frete = forms.DecimalField(decimal_places=2, label='Frete Valor', initial=100)
    precificacaoId = forms.ChoiceField(label='Método de Precificação', required=True, initial=None)
    status = forms.ChoiceField(label='Situação', choices=TIPO_COTACAO_STATUS, initial=True)
    # created_dt = forms.DateTimeField(label='Data do cadastro', required=False)
    # valorItem = forms.DecimalField(decimal_places=2, label='Valor dos Itens', initial=0, disabled=True)

    def __init__(self, *args, request, uuid=None, cotacao=None, **kwargs):
        super(CotacaoOrcamentoForm, self).__init__(*args, **kwargs)
        self.fields['precificacaoId'].choices = precificacaoChoices(request)

    def salvar(self, request, uuid=None):
        data = dados_para_json(self.data, nones=[])
        headers = session_get_headers(request)
        response = requests.post(
            URL_RECURSO + str(uuid) + "/orcamento", json=data, headers=headers)
        if not response.status_code in [200, 201]:
            raise Exception(tratar_error(response))


@require_token
def cotacaoOrcamentoNew(request, uuid):
    return cotacao_orcamento_render(request=request, cotacao=uuid)


@require_token
def cotacaoOrcamentoEdit(request, uuid):
    return cotacao_orcamento_render(request, uuid, None)


@require_token
def cotacao_orcamento_render(request, uuid=None, cotacao=None):
    template_name = 'compra/cotacao_orcamento.html'
    form = CotacaoOrcamentoForm(request=request, uuid=uuid, cotacao=cotacao)
    return render(request, template_name, {'form': form})

