import json

import requests
from django.http import HttpResponseRedirect
from django.urls import reverse

from core.controle import session_get_headers, tratar_error
from core.settings import URL_API
from pessoa.models import PessoaModel, PESSOA_FIELDS, CLIENTE_FIELDS, FORNECEDOR_FIELDS, TRANSPORTADOR_FIELDS, \
    VENDEDOR_FIELDS
from django import forms


# Create your tests here.

class PessoaForm(forms.ModelForm):
    class Meta:
        model = PessoaModel
        fields = '__all__'
        exclude = ['created_dt',
                   'updated_dt'] + CLIENTE_FIELDS + FORNECEDOR_FIELDS + TRANSPORTADOR_FIELDS + VENDEDOR_FIELDS
        widgets = {
            'emissao': forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control'}),
            'nascimento': forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control'}),
            'fundacao': forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control'})
        }

    def existe(self):
        return existe_registro(self, self.data, 'pessoaId')

    def ativar(self, request, uuid):
        ativar_pessoa_tipo(self, request, 'pessoa', uuid)

    def salvar(self, request, uuid=None):
        data = self.json()
        if self.is_valid():
            headers = session_get_headers(request)
            if uuid:
                response = requests.patch(URL_API + 'pessoa/' + str(uuid), json=data, headers=headers)
            else:
                response = requests.post(URL_API + 'pessoa', json=data, headers=headers)
            if response.status_code in [200, 201]:
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
        fields = PESSOA_FIELDS + CLIENTE_FIELDS

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['autofocus'] = True
        self.fields['emailFiscal'].required = False

    def existe(self):
        return existe_registro(self, self.initial, 'clienteId')

    def pesquisaPorPessoa(self, request, uuid):
        self.initial = pesquisa_pessoa(self, request, uuid, 'cliente')

    def json(self):
        post_data = dict(self.data)  # Converter QueryDict para dicionário
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        json_data = json.dumps(post_data).replace("[", "").replace("]", "")
        data = json.loads(json_data)
        if data['clienteId'] == 'None': data['clienteId'] = None
        return data

    def ativar(self, request, uuid):
        ativar_pessoa_tipo(self, request, 'cliente', uuid)

    def salvar(self, request):
        data = self.json()
        salvar_pessoa_tipo(self, request, data, 'cliente')


class FornecedorForm(forms.ModelForm):
    codigo = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = PessoaModel
        fields = PESSOA_FIELDS + FORNECEDOR_FIELDS

    def __init__(self, *args, **kwargs):
        super(FornecedorForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['autofocus'] = True
        self.fields['email'].required = False

    def existe(self):
        return existe_registro(self, self.initial, 'fornecedorId')

    def pesquisaPorPessoa(self, request, uuid):
        self.initial = pesquisa_pessoa(self, request, uuid, 'fornecedor')

    def json(self):
        post_data = dict(self.data)  # Converter QueryDict para dicionário
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        json_data = json.dumps(post_data).replace("[", "").replace("]", "")
        data = json.loads(json_data)
        if data['fornecedorId'] == 'None': data['fornecedorId'] = None
        return data

    def ativar(self, request, uuid):
        ativar_pessoa_tipo(self, request, 'fornecedor', uuid)

    def salvar(self, request):
        data = self.json()
        salvar_pessoa_tipo(self, request, data, 'fornecedor')


# TRANSPORTADOR
class TransportadorForm(forms.ModelForm):
    codigo = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = PessoaModel
        fields = PESSOA_FIELDS + TRANSPORTADOR_FIELDS

    def __init__(self, *args, **kwargs):
        super(TransportadorForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['autofocus'] = True
        self.fields['email'].required = False

    def existe(self):
        return existe_registro(self, self.initial, 'transportadorId')

    def pesquisaPorPessoa(self, request, uuid):
        self.initial = pesquisa_pessoa(self, request, uuid, 'transportador')

    def json(self):
        post_data = dict(self.data)  # Converter QueryDict para dicionário
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        json_data = json.dumps(post_data).replace("[", "").replace("]", "")
        data = json.loads(json_data)
        if data['transportadorId'] == 'None': data['transportadorId'] = None
        return data

    def ativar(self, request, uuid):
        ativar_pessoa_tipo(self, request, 'transportador', uuid)

    def salvar(self, request):
        data = self.json()
        salvar_pessoa_tipo(self, request, data, 'transportador')


# VENDEDOR
class VendedorForm(forms.ModelForm):
    codigo = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = PessoaModel
        fields = PESSOA_FIELDS + VENDEDOR_FIELDS

    def __init__(self, *args, **kwargs):
        super(VendedorForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['autofocus'] = True
        self.fields['email'].required = False

    def existe(self):
        return existe_registro(self, self.initial, 'vendedorId')

    def pesquisaPorPessoa(self, request, uuid):
        self.initial = pesquisa_pessoa(self, request, uuid, 'vendedor')

    def json(self):
        post_data = dict(self.data)  # Converter QueryDict para dicionário
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        json_data = json.dumps(post_data).replace("[", "").replace("]", "")
        data = json.loads(json_data)
        if data['vendedorId'] == 'None': data['vendedorId'] = None
        return data

    def ativar(self, request, uuid):
        ativar_pessoa_tipo(self, request, 'vendedor', uuid)

    def salvar(self, request):
        data = self.json()
        salvar_pessoa_tipo(self, request, data, 'vendedor')


# FUNCÕES AUXILIARES
def existe_registro(self, dados, campo):
    return True if dados.get(campo) and dados.get(campo) != 'None' else False


def pesquisa_pessoa(self, request, uuid, tipo):
    response = requests.get(URL_API + 'pessoa/' + str(uuid) + "/" + tipo, headers=session_get_headers(request))
    if response.status_code == 200:
        return response.json()
    else:
        response = requests.get(URL_API + 'pessoa/' + str(uuid), headers=session_get_headers(request))
        if response.status_code == 200:
            return response.json()


def ativar_pessoa_tipo(self, request, tipo, uuid):
    headers = session_get_headers(request)
    url = URL_API + tipo + '/' + str(uuid) + "/ativar-inativar"
    response = requests.patch(url, headers=headers)
    if not response.status_code in [200]:
        raise Exception(tratar_error(response))


def salvar_pessoa_tipo(self, request, data, tipo):
    uuid = data[tipo + 'Id']
    headers = session_get_headers(request)
    if uuid and uuid != 'None':
        response = requests.patch(URL_API + tipo + '/' + str(uuid), json=data, headers=headers)
    else:
        response = requests.post(URL_API + tipo, json=data, headers=headers)

    if not response.status_code in [200, 201]:
        raise Exception(tratar_error(response))


class PessoaListForm(forms.Form):
    nome = forms.CharField(label='Pesquisa')

    def pesquisar(self, request):
        headers = session_get_headers(request)
        response = requests.get(URL_API + 'pessoa', headers=headers)
        data = response.json()
        return data['content'] if 'content' in data else []

