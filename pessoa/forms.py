import json
from urllib.parse import urlencode

import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from core.controle import format_cnpj, format_cpf, session_get_headers, tratar_error
from core.paginacao import get_page
from core.settings import URL_API
from core.tipos import TIPO_PROPRIETARIO
from pessoa.models import TIPO_SITUACAO, TIPO_CHOICES, cpf_regex, cnpj_regex, TIPO_SIM_NAO, REGIME_TRIBUTARIO_CHOICES, \
    TIPO_CONTRIBUINTE_CHOICES

# Create your tests here.

class PessoaForm(forms.Form):
    pessoaId = forms.IntegerField(label='Pessoa ID', required=False)
    nome = forms.CharField(max_length=100, label='Nome', widget=forms.DateInput(attrs={'autofocus': 'true', }))
    fone = forms.CharField(max_length=20, label='Fone')
    email = forms.EmailField(max_length=254, label='E-mail')
    situacaoPessoa = forms.ChoiceField(label='Situação', choices=TIPO_SITUACAO, initial=True)
    tipoPessoa = forms.ChoiceField(choices=TIPO_CHOICES, initial='INDEFINIDO', label='Tipo')
    created_dt = forms.DateTimeField(required=False)
    updated_dt = forms.DateTimeField(required=False)
    # definição para pessoa física
    cpf = forms.CharField(max_length=14, required=False, validators=[cpf_regex], label='CPF')
    identidade = forms.CharField(max_length=20, required=False, label='Identidade')
    pai = forms.CharField(max_length=100, required=False, label='Pai')
    mae = forms.CharField(max_length=100, required=False, label='Nome da Mãe')
    nascimento = forms.DateField(label='Nascimento', required=False,
                                 widget=forms.DateInput(
                                     attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control', }))
    emissao = forms.DateField(label='Emissão', required=False,
                              widget=forms.DateInput(
                                  attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control', }))
    orgao = forms.CharField(max_length=10, required=False, label='Órgão')
    idEstrangeiro = forms.CharField(max_length=10, required=False,
                                    label='Id.Estrangeiro')
    nacionalidade = forms.CharField(max_length=30, required=False, label='Nacionalidade')
    naturalidade = forms.CharField(max_length=30, required=False, label='Naturalidade')
    # definição para pessoa jurídica
    cnpj = forms.CharField(max_length=18, required=False, validators=[cnpj_regex], label='CNPJ')
    fantasia = forms.CharField(max_length=100, required=False, label='Nome de Fantasia')
    IE = forms.CharField(max_length=20, required=False, label='Insc.Estadual')
    cnae = forms.CharField(max_length=20, required=False, label='CNAE')
    fundacao = forms.DateField(label='Data Fundação', required=False,
                               widget=forms.DateInput(
                                   attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy', 'class': 'form-control', }))
    incentivoCultural = forms.ChoiceField(label='Incentivo Cult.', required=False, choices=TIPO_SIM_NAO)
    regime = forms.ChoiceField(choices=REGIME_TRIBUTARIO_CHOICES,
                               initial=REGIME_TRIBUTARIO_CHOICES[0][0],
                               label='Reg.Tributário')
    tipoIE = forms.ChoiceField(choices=TIPO_CONTRIBUINTE_CHOICES,
                               initial=TIPO_CONTRIBUINTE_CHOICES[0][0],
                               label='Contribuinte')
    # Endereçamento
    uf = forms.CharField(required=False)
    enderecoId = forms.IntegerField(required=False)
    municipioId = forms.ChoiceField(choices=(), initial=2304400, label='Município')
    estado = forms.ChoiceField(choices=(), initial='CE', label='Estado', required=False)
    cep = forms.CharField(max_length=9, min_length=8, label='CEP', required=True, initial='60000000')
    bairro = forms.CharField(max_length=60, min_length=3, label='Bairro', required=False, initial='centro')
    logradouro = forms.CharField(max_length=60, min_length=3, label='Logradouro', required=False, initial='rua do beco')
    referencia = forms.CharField(max_length=100, label='Referência', required=False)
    complemento = forms.CharField(max_length=60, label='Complemento', required=False)
    numero = forms.IntegerField(label='Número', initial=100, required=False)
    clienteId = forms.IntegerField(label='Cliente', required=False)
    vendedorId = forms.IntegerField(label='Vendedor', required=False)
    transportadorId = forms.IntegerField(label='Transportador', required=False)
    fornecedorId = forms.IntegerField(label='Fornecedor', required=False)

    def __init__(self, *args, request, uuid=None, **kwargs):
        super(PessoaForm, self).__init__(*args, **kwargs)
        if uuid:
            response = requests.get(URL_API + 'pessoa/' + str(uuid), headers=session_get_headers(request))
            if response.status_code == 200:
                self.initial = response.json()
                if self.data.get('cpf'):
                    self.data['cpf'] = format_cpf(self.data.get('cpf'))
                if self.data.get('cnpj'):
                    self.data['cnpj'] = format_cnpj(self.data.get('cnpj'))
            else:
                raise Exception(tratar_error(response))

    def municipios(self, request, uf):
        municipios = []
        response = requests.get(URL_API + 'municipio/estado/' + str(uf), headers=session_get_headers(request))
        if response.status_code == 200:
            for n in response.json():
                municipios.append((n['id'], n['descricao']))
        return municipios    

    def existe(self):
        return existe_registro(self, self.data, 'pessoaId')

    def ativar(self, request, uuid):
        ativar_pessoa_tipo(self, request, 'pessoa', uuid)

    def salvar(self, request, uuid=None):
        data = self.json()
        headers = session_get_headers(request)
        if uuid:
            response = requests.patch(URL_API + 'pessoa/' + str(uuid), json=data, headers=headers)
        else:
            response = requests.post(URL_API + 'pessoa', json=data, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()['pessoaId']
        else:
            raise Exception(tratar_error(response))

    def json(self):
        post_data = dict(self.data)  # Converter QueryDict para dicionário
        post_data.pop('csrfmiddlewaretoken', None)
        post_data.pop('btn_salvar', None)
        # pessoa fisica
        if self.data.get('tipoPessoa') == 'FISICA':
            cpf = str(self.data.get('cpf'))
            post_data['cpf'] = ''.join(filter(str.isdigit, cpf))
        else:
            post_data.pop('cpf', None)
            post_data.pop('identidade', None)
            post_data.pop('orgao', None)
            post_data.pop('pai', None)
            post_data.pop('mae', None)

        # pessoa jurídica
        if self.data.get('tipoPessoa') == 'JURIDICA':
            cnpj = str(self.data.get('cnpj'))
            post_data['cnpj'] = ''.join(filter(str.isdigit, cnpj))
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
        data = json.loads(json_data)
        if data['enderecoId'] == 'None': data['enderecoId'] = None
        if data['clienteId'] == 'None': data['clienteId'] = None
        if data['vendedorId'] == 'None': data['vendedorId'] = None
        if data['transportadorId'] == 'None': data['transportadorId'] = None
        if data['fornecedorId'] == 'None': data['fornecedorId'] = None
        return data

class ClienteForm(forms.Form):
    pessoaId = forms.IntegerField()
    nome = forms.CharField(max_length=100, label='Nome', disabled=True)    
    clienteId = forms.IntegerField(label='Código', required=False, disabled=True)
    situacaoCliente = forms.ChoiceField(choices=TIPO_SITUACAO, initial=True)
    emailFiscal = forms.EmailField(label='E-mail Fiscal', required=False, widget=forms.DateInput(attrs={'autofocus': 'true', }))
    limiteCredito = forms.FloatField(label='Limite de Crédito', initial=0)
    limitePrazo = forms.FloatField(label='Limite de Prazo', initial=0)
    retencaoIss = forms.ChoiceField(choices=TIPO_SIM_NAO, initial=False, label='Retenção ISS')

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


class FornecedorForm(forms.Form):
    pessoaId = forms.IntegerField()
    nome = forms.CharField(max_length=100, label='Nome', disabled=True)    
    fornecedorId = forms.IntegerField(label='Código', required=False, disabled=True)
    situacaoFornecedor = forms.ChoiceField(choices=TIPO_SITUACAO, initial=True)
    created_dt = forms.DateTimeField(label='Data do cadastro', required=False)

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
class TransportadorForm(forms.Form):
    pessoaId = forms.IntegerField()
    nome = forms.CharField(max_length=100, label='Nome', disabled=True)
    transportadorId = forms.IntegerField(label='Código', required=False, disabled=True)
    situacaoTransportador = forms.ChoiceField(choices=TIPO_SITUACAO, initial=True)
    codigoRNTRC = forms.CharField(max_length=20, label='RNTRC', required=False) 
    tipoProprietario = forms.ChoiceField(choices=TIPO_PROPRIETARIO, initial="OUTROS", label="Tipo de Proprietário")
    created_dt = forms.DateTimeField(label='Data do cadastro', required=False)

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
class VendedorForm(forms.Form):
    pessoaId = forms.IntegerField()
    nome = forms.CharField(max_length=100, label='Nome', disabled=True)
    vendedorId = forms.IntegerField(label='Código', required=False, disabled=True)
    situacaoVendedor = forms.ChoiceField(choices=TIPO_SITUACAO, initial=True)
    comissao = forms.FloatField(label='Percentual de Comissão', initial=0, widget=forms.DateInput(attrs={'autofocus': 'true', }))
    created_dt = forms.DateTimeField(label='Data do cadastro', required=False)

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
    url = URL_API + 'pessoa/' + str(uuid)
    if tipo:
        response = requests.get(url +"/" +tipo, headers=session_get_headers(request))
        return response.json()
    else:
        response = requests.get(url, headers=session_get_headers(request))
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
    descricao = forms.CharField(label='Pesquisa', required=False,
                           widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    def pesquisar(self, request, params):
        headers = session_get_headers(request)
        response = requests.get(URL_API + 'pessoa', headers=headers, params=params)
        if response.status_code == 200:
            self.fields['descricao'].initial = self.initial.get('descricao')
            self.initial = dict(response.json())
            return get_page(self.initial, params)    

