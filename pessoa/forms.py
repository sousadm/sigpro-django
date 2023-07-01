import json

import requests
from django.urls import reverse

from core.controle import session_get_token, session_get_headers, tratar_error
from core.settings import URL_API
from pessoa.models import PessoaModel, TIPO_CHOICES
from django import forms
from decimal import Decimal

# Create your tests here.


class PessoaForm(forms.ModelForm):
    class Meta:
        model = PessoaModel
        fields = '__all__'
        exclude = ['created_dt','updated_dt', 'clienteId', 'emailFiscal', 'retencaoIss', 'limiteCredito', 'limitePrazo','situacaoCliente']
        widgets = {
            'emissao': forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control'}),
            'nascimento': forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control'}),
            'fundacao': forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control'})
        }

    def existe(self):
        return True if self.data.get('pessoaId') and self.data.get('pessoaId') != 'None' else False

    def ativar(self, request):
        headers = session_get_headers(request)
        url = URL_API + 'pessoa/' + str(self.data['pessoaId']) + "/ativar-inativar"
        response = requests.patch(url, headers=headers)
        if not response.status_code in [200]:
            raise Exception(tratar_error(response))

    def salvar(self, request, uuid=None):
        data = self.json()
        if self.is_valid():
            headers = session_get_headers(request)
            if uuid:
                response = requests.patch(URL_API + 'pessoa/'+str(uuid), json=data, headers=headers)
            else:
                response = requests.post(URL_API+'pessoa', json=data, headers=headers)
            if response.status_code in [200,201]:
                return response.json()['pessoaId']
            else:
                raise Exception(tratar_error(response))
        else:
            raise ValueError(self.errors)

    def __init__(self, *args, **kwargs):
        super(PessoaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['autofocus'] = True
        self.fields['pessoaId'].widget.attrs['disabled'] = 'disabled'
        self.fields['pessoaId'].required = False
        # atributos de pessoa jurídica
        self.fields['cpf'].required = False
        self.fields['identidade'].required = False
        self.fields['emissao'].required = False
        self.fields['nascimento'].required = False
        self.fields['pai'].required = False
        self.fields['mae'].required = False
        self.fields['orgao'].required = False
        self.fields['idEstrangeiro'].required = False
        self.fields['nacionalidade'].required = False
        self.fields['naturalidade'].required = False
        # atributos de pessoa jurídica
        self.fields['cnpj'].required = False
        self.fields['fantasia'].required = False
        self.fields['IE'].required = False
        self.fields['cnae'].required = False
        self.fields['fundacao'].required = False
        self.fields['incentivoCultural'].required = False
        self.fields['regime'].required = False
        self.fields['tipoIE'].required = False

    def json(self):
        post_data = dict(self.data)  # Converter QueryDict para dicionário
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        # pessoa fisica
        if self.data.get('tipoPessoa') == 'FISICA':
            cpf = str(self.data.get('cpf'))
            post_data['cpf'] = cpf.replace('.', '').replace('-', '')
        else:
            post_data.pop('cpf', None)
            post_data.pop('identidade', None)
            post_data.pop('orgao', None)
            post_data.pop('pai', None)
            post_data.pop('mae', None)

        # pessoa jurídica
        if self.data.get('tipoPessoa') == 'JURIDICA':
            cnpj = str(self.data.get('cnpj'))
            post_data['cnpj'] = cnpj.replace('.', '').replace('-', '').replace('/', '')
        else:
            post_data.pop('cnpj', None)
            post_data.pop('fantasia', None)
            post_data.pop('IE', None)
            post_data.pop('cnae', None)
            post_data.pop('fundacao', None)
            post_data.pop('incentivoCultural', None)
            post_data.pop('regime', None)
            post_data.pop('tipoIE', None)

        json_data = json.dumps(post_data).replace("[", "").replace("]", "")
        return json.loads(json_data)

class ClienteForm(forms.ModelForm):
    codigo = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = PessoaModel
        fields = [
            'nome',
            'email',
            'fone',
            'pessoaId',
            'clienteId',
            'emailFiscal',
            'retencaoIss',
            'limiteCredito',
            'limitePrazo',
            'situacaoCliente'
        ]

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['autofocus'] = True
        self.fields['clienteId'].widget.attrs['disabled'] = 'disabled'

    def pesquisaPorPessoa(self, request, uuid):
        if uuid:
            response = requests.get(URL_API + 'pessoa/' + str(uuid) + "/cliente", headers=session_get_headers(request))
            if response.status_code == 200:
                self.initial = response.json()
            else:
                response = requests.get(URL_API + 'pessoa/' + str(uuid), headers=session_get_headers(request))
                if response.status_code == 200:
                    self.initial = response.json()

    def json(self):
        post_data = dict(self.data)  # Converter QueryDict para dicionário
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        json_data = json.dumps(post_data).replace("[", "").replace("]", "")
        return json.loads(json_data)

    def salvar(self, request, uuid):
        data = self.json()
        clienteId = data['clienteId']
        headers = session_get_headers(request)
        if clienteId:
            response = requests.patch(URL_API + 'cliente/'+str(clienteId), json=data, headers=headers)
        else:
            response = requests.post(URL_API+'cliente', json=data, headers=headers)
        if not response.status_code in [200,201]:
            raise Exception(tratar_error(response))
