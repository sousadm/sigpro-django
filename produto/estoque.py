import requests
from django import forms
from django.contrib import messages
from django.shortcuts import render

from core.controle import session_get_headers, tratar_error, dados_para_json, require_token
from core.settings import URL_API
from produto.distribuicao import centroDistribuicaoChoices

URL_RECURSO = URL_API + 'estoque/'

TIPO_ESTOQUE_MOVIMENTO = (
    ('ENTRADA', 'Entrada'),
    ('SAIDA', 'Saída')
)

class EstoqueForm(forms.Form):
    descricao = forms.CharField(label='Descrição do Produto', disabled=True, required=False)
    estoque = forms.DecimalField(label="Estoque atual", disabled=True, required=False, min_value=0, decimal_places=2, initial=0)
    produtoId = forms.IntegerField(label='Código do Produto', disabled=True, required=False)
    historico = forms.CharField(max_length=100, label='Histórico de movimentação', required=True, widget=forms.DateInput(attrs={'autofocus': 'true',}))
    documento = forms.CharField(max_length=10, label='Documento')
    quantidade = forms.DecimalField(label="Quantidade", min_value=0, decimal_places=2, initial=1)
    centroDistribuicaoId = forms.ChoiceField(label='Centro de Distribuição', initial=None)
    tipo = forms.ChoiceField(choices=TIPO_ESTOQUE_MOVIMENTO, label='Tipo de Movimentação', initial='ENTRADA')

    def __init__(self, *args, request, uuid, **kwargs):
        super(EstoqueForm, self).__init__(*args, **kwargs)
        self.fields['centroDistribuicaoId'].choices = centroDistribuicaoChoices(request)
        response = requests.get(URL_API + 'produto/' + str(uuid), headers=session_get_headers(request))
        data = dict(response.json())
        print(data)
        if response.status_code == 200:
            self.fields['descricao'].initial = data.get('descricao')
            self.fields['produtoId'].initial = data.get('id')
            self.fields['estoque'].initial = data.get('estoque', 0)
        else:
            raise Exception(tratar_error(response))

    def salvar(self, request, uuid=None):
        data = dados_para_json(self.data)
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
def produtoEstoque(request, uuid):
    template_name = 'produto/produto_estoque.html'
    try:
        if request.POST.get('btn_salvar'):
            form = EstoqueForm(request.POST, request=request)
            uuid = form.salvar(request, uuid)
            messages.success(request, 'sucesso ao gravar dados')
    except Exception as e:
        messages.error(request, e)
    form = EstoqueForm(request=request, uuid=uuid)
    return render(request, template_name, {'form': form})


