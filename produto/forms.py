import requests
from django import forms

from core.controle import session_get_headers, tratar_error
from core.settings import URL_API
from produto.models import Categoria

TIPO_CATEGORIA = (
    ('REVENDA','Produtos para revenda'),
    ('CONSUMO','Produtos para consumo'),
    ('INSUMOS','Insumos de produção'),
    ('IMOBILIZADO','Ativos imobilizado'),
    ('SERVICO','Serviços'),
)

class PessoaForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False)
    descricao = forms.CharField(max_length=100, label='Descrição', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    tipoPessoa = forms.ChoiceField(choices=TIPO_CATEGORIA, initial='INDEFINIDO', label='Tipo')

    def salvar(self, request, uuid=None):
        data = Categoria(**self.json())
        headers = session_get_headers(request)
        if uuid:
            response = requests.patch(URL_API + 'categoria/' + str(uuid), json=data, headers=headers)
        else:
            response = requests.post(URL_API + 'categoria', json=data, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()['id']
        else:
            raise Exception(tratar_error(response))