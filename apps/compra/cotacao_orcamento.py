import requests
from django.contrib import messages
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from core.controle import dados_para_json, require_token, session_get_headers, tratar_error
from core.settings import URL_API
from apps.produto.precificacao import precificacaoChoices

URL_RECURSO = URL_API + 'cotacao/'
URL_RECURSO_ORCAMENTO = URL_API + 'cotacao-orcamento/'

TIPO_COTACAO_STATUS = (
	('EM_ANALISE', 'Em anállise'), 
    ('APROVADO', 'Aprovado'), 
    ('CANCELADO', 'Cancelado'),
)

class CotacaoOrcamentoForm(forms.Form):
    orcamentoId = forms.IntegerField(label='ID', required=False)
    nome = forms.CharField(label='Nome do Fornecedor', max_length=100)
    documento = forms.CharField(label='Documento', max_length=14, required=False, widget=forms.DateInput(attrs={'title': 'digite o CPF ou CNPJ', }))
    observacao = forms.CharField(label='Observação', max_length=100, required=False)
    email = forms.EmailField(label='E-mail')
    fone = forms.CharField(label='Fone', max_length=20)
    desconto = forms.DecimalField(decimal_places=2, initial=0)
    frete = forms.DecimalField(decimal_places=2, initial=0)
    precificacaoId = forms.ChoiceField(label='Método de Precificação', required=True, initial=None)
    status = forms.ChoiceField(label='Situação', choices=TIPO_COTACAO_STATUS, initial=True, disabled=True)

    def __init__(self, *args, request, uuid=None, cotacao=None, **kwargs):
        super(CotacaoOrcamentoForm, self).__init__(*args, **kwargs)
        self.fields['precificacaoId'].choices = precificacaoChoices(request)
        response = requests.get(URL_RECURSO_ORCAMENTO + str(uuid), headers=session_get_headers(request))
        if response.status_code == 200:
            data = dict(response.json())
            self.initial = data        

    def salvar(self, request, uuid=None, orcamentoId=None):
        data = dados_para_json(self.data, nones=['orcamentoId','btn_orcamento_salvar','btn_orcamento_salvar'])
        headers = session_get_headers(request)
        if not orcamentoId or orcamentoId == 'None':
            response = requests.post(URL_RECURSO + str(uuid) + "/orcamento", json=data, headers=headers)
        else:
            response = requests.patch(URL_RECURSO_ORCAMENTO + str(orcamentoId), json=data, headers=headers)
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


@require_token
def cotacaoOrcamentoDelete(request, uuid, orcamento):
    response = requests.delete(URL_RECURSO_ORCAMENTO + str(orcamento), headers=session_get_headers(request))
    if response.status_code == 200:
        messages.success(request, 'orçamento excluído com sucesso')
    else:
        messages.error(request, Exception(tratar_error(response)))
    return HttpResponseRedirect(reverse('url_cotacao_edit', kwargs={'uuid': uuid}))

