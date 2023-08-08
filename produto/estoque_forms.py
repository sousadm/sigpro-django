import requests
from django import forms

from core.controle import session_get_headers, tratar_error
from core.settings import URL_API

URL_RECURSO = URL_API + 'estoque/'

TIPO_ESTOQUE_MOVIMENTO = (
    ('ENTRADA', 'Entrada'),
    ('SAIDA', 'Saída')
)

class EstoqueForm(forms.Form):
    produtoId = forms.IntegerField(label='Código do Produto', required=True, widget=forms.DateInput(attrs={'autofocus': 'true', }))
    historico = forms.CharField(max_length=100, label='Histórico de movimentação', required=True)
    documento = forms.CharField(max_length=10, label='Histórico de movimentação')
    quantidade = forms.DecimalField(label="Quantidade", min_value=0, decimal_places=2, initial=1)
    tipo = forms.ChoiceField(choices=TIPO_ESTOQUE_MOVIMENTO, label='Tipo de Movimentação', initial='ENTRADA')

    def __init__(self, *args, request, uuid, **kwargs):
        super(EstoqueForm, self).__init__(*args, **kwargs)
        response = requests.get(URL_API + 'produto/' + str(uuid), headers=session_get_headers(request))
        print(response.json())
        if response.status_code == 200:
            self.initial = response.json()
        else:
            raise Exception(tratar_error(response))

    def salvar(self, request, uuid=None):
        data = self.json()
        headers = session_get_headers(request)
        if uuid:
            response = requests.patch(URL_RECURSO + str(uuid), json=data, headers=headers)
        else:
            response = requests.post(URL_RECURSO, json=data, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()['id']
        else:
            raise Exception(tratar_error(response))
