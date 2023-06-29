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
        exclude = ['created_dt','updated_dt']
        widgets = {
            'emissao': forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control'}),
            'nascimento': forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control'}),
            'fundacao': forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control'})
        }

    def salvar(self, request, uuid=None):
        if self.is_valid():
            headers = session_get_headers(request)
            if uuid:
                response = requests.patch(URL_API + 'pessoa/'+str(uuid), json=self.json(), headers=headers)
            else:
                response = requests.post(URL_API+'pessoa', json=self.json(), headers=headers)
            if response.status_code in [200,201]:
                return response.json()['uuid']
            else:
                raise Exception(tratar_error(response))
        else:
            raise ValueError(self.errors)

    def __init__(self, *args, **kwargs):
        super(PessoaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['autofocus'] = True
        self.fields['uuid'].widget.attrs['disabled'] = 'disabled'
        self.fields['uuid'].required = False
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

    def define_cliente_url(self):
        if self.data.get('uuid'):
            return reverse("url_define_cliente", kwargs={"uuid": self.data.get('uuid')})
        else:
            return None


class ClienteForm(forms.ModelForm):
    class Meta:
        model = PessoaModel
        fields = [
            'nome',
            'clienteId',
            'emailFiscal',
            'retencaoIss',
            'limiteCredito',
            'limitePrazo',
        ]
    def pesquisaPorPessoa(self, request, uuid):
        response = requests.get(URL_API + 'pessoa/' + str(uuid) + "/cliente", headers=session_get_headers(request))
        if response.status_code == 200:
            self.initial = response.json()

